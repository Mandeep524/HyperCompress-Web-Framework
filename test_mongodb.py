"""
Quick test to verify MongoDB connection
"""

from utils.database import CompressionDB

try:
    print("🔌 Testing MongoDB connection...")
    db = CompressionDB()
    
    # Test storing a file
    print("\n📝 Testing file storage...")
    file_id = db.store_file(
        file_data=b"Hello, MongoDB!",
        filename="test.txt",
        file_type="text/plain"
    )
    print(f"✅ File stored with ID: {file_id}")
    
    # Test retrieving the file
    print("\n📥 Testing file retrieval...")
    retrieved_data = db.get_file(file_id)
    print(f"✅ File retrieved: {retrieved_data.decode()}")
    
    # Test storing a compression record
    print("\n💾 Testing compression record...")
    record = {
        'filename': 'test.txt',
        'file_type': 'text',
        'algorithm': 'Test',
        'original_size': 100,
        'compressed_size': 50,
        'compression_ratio': 0.5,
        'space_savings': 50.0,
        'compression_time': 0.001,
        'decompression_time': 0.001,
        'original_file_id': file_id,
        'compressed_file_id': file_id
    }
    record_id = db.save_compression_record(record)
    print(f"✅ Record saved with ID: {record_id}")
    
    # Test getting statistics
    print("\n📊 Testing statistics...")
    stats = db.get_statistics()
    print(f"✅ Total compressions: {stats.get('total_compressions', 0)}")
    
    # Test getting history
    print("\n📜 Testing history...")
    history = db.get_compression_history(limit=5)
    print(f"✅ Found {len(history)} history records")
    
    print("\n🎉 All tests passed! MongoDB is connected and working!")
    print(f"\n📍 Database: compression_project")
    print(f"📍 Connection: mongodb://localhost:27017/")
    print(f"📍 Collections: compression_history, files, fs.files, fs.chunks")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n⚠️  Make sure MongoDB is running:")
    print("   brew services start mongodb-community")
    print("   or")
    print("   mongod")
