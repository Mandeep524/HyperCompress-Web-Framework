"""
MongoDB Database Utility for Compression Project
Stores uploaded files, compressed data, and compression history
"""

from pymongo import MongoClient
from datetime import datetime
import gridfs
import os

class CompressionDB:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """Initialize MongoDB connection"""
        self.client = MongoClient(connection_string)
        self.db = self.client['compression_project']
        
        # Collections
        self.compression_history = self.db['compression_history']
        self.files = self.db['files']
        
        # GridFS for large file storage
        self.fs = gridfs.GridFS(self.db)
        
        # Create indexes
        self.compression_history.create_index([('timestamp', -1)])
        self.compression_history.create_index([('file_type', 1)])
        self.compression_history.create_index([('algorithm', 1)])
    
    def store_file(self, file_data, filename, file_type):
        """Store original file in GridFS"""
        # Extract file extension
        file_extension = os.path.splitext(filename)[1] if '.' in filename else ''
        
        file_id = self.fs.put(
            file_data,
            filename=filename,
            file_type=file_type,
            file_extension=file_extension,
            upload_date=datetime.now()
        )
        return str(file_id)
    
    def store_compressed_file(self, compressed_data, filename, algorithm):
        """Store compressed file in GridFS"""
        # Extract file extension from original filename
        file_extension = os.path.splitext(filename)[1] if '.' in filename else ''
        compressed_filename = f"{os.path.splitext(filename)[0]}_{algorithm}_compressed{file_extension}"
        
        file_id = self.fs.put(
            compressed_data,
            filename=compressed_filename,
            algorithm=algorithm,
            file_extension=file_extension,
            upload_date=datetime.now()
        )
        return str(file_id)
    
    def get_file(self, file_id):
        """Retrieve file from GridFS"""
        from bson.objectid import ObjectId
        try:
            file_data = self.fs.get(ObjectId(file_id))
            return file_data.read()
        except Exception as e:
            print(f"Error retrieving file: {e}")
            return None
    
    def get_file_metadata(self, file_id):
        """Retrieve file metadata from GridFS"""
        from bson.objectid import ObjectId
        try:
            file_obj = self.fs.get(ObjectId(file_id))
            return {
                'filename': file_obj.filename,
                'file_extension': getattr(file_obj, 'file_extension', ''),
                'file_type': getattr(file_obj, 'file_type', ''),
                'algorithm': getattr(file_obj, 'algorithm', ''),
                'upload_date': file_obj.upload_date
            }
        except Exception as e:
            print(f"Error retrieving file metadata: {e}")
            return None
    
    def save_compression_record(self, record):
        """Save compression operation record to history"""
        record['timestamp'] = datetime.now()
        result = self.compression_history.insert_one(record)
        return str(result.inserted_id)
    
    def get_compression_history(self, limit=50, file_type=None, algorithm=None):
        """Get compression history with optional filters"""
        query = {}
        if file_type:
            query['file_type'] = file_type
        if algorithm:
            query['algorithm'] = algorithm
        
        cursor = self.compression_history.find(query).sort('timestamp', -1).limit(limit)
        history = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            if 'original_file_id' in doc:
                doc['original_file_id'] = str(doc['original_file_id'])
            if 'compressed_file_id' in doc:
                doc['compressed_file_id'] = str(doc['compressed_file_id'])
            history.append(doc)
        return history
    
    def get_statistics(self):
        """Get overall compression statistics"""
        total_compressions = self.compression_history.count_documents({})
        
        # Count by algorithm
        algorithm_stats = {}
        for algo in ['RLE', 'Huffman', 'LZW']:
            count = self.compression_history.count_documents({'algorithm': algo})
            algorithm_stats[algo] = count
        
        # Count by file type
        file_type_stats = {}
        for ftype in ['text', 'image', 'video', 'document']:
            count = self.compression_history.count_documents({'file_type': ftype})
            file_type_stats[ftype] = count
        
        # Average compression ratios
        pipeline = [
            {
                '$group': {
                    '_id': '$algorithm',
                    'avg_ratio': {'$avg': '$compression_ratio'},
                    'avg_savings': {'$avg': '$space_savings'}
                }
            }
        ]
        avg_stats = list(self.compression_history.aggregate(pipeline))
        
        return {
            'total_compressions': total_compressions,
            'algorithm_stats': algorithm_stats,
            'file_type_stats': file_type_stats,
            'average_stats': avg_stats
        }
    
    def delete_record(self, record_id):
        """Delete a compression record and associated files"""
        from bson.objectid import ObjectId
        try:
            record = self.compression_history.find_one({'_id': ObjectId(record_id)})
            if record:
                # Delete associated files
                if 'original_file_id' in record:
                    self.fs.delete(ObjectId(record['original_file_id']))
                if 'compressed_file_id' in record:
                    self.fs.delete(ObjectId(record['compressed_file_id']))
                
                # Delete record
                self.compression_history.delete_one({'_id': ObjectId(record_id)})
                return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
    
    def clear_old_records(self, days=30):
        """Clear records older than specified days"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        old_records = self.compression_history.find({'timestamp': {'$lt': cutoff_date}})
        count = 0
        for record in old_records:
            if self.delete_record(str(record['_id'])):
                count += 1
        
        return count
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()


# Singleton instance
_db_instance = None

def get_db():
    """Get or create database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = CompressionDB()
    return _db_instance
