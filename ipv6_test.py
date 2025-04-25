import socket

try:
    s = socket.socket(socket.AF_INET6)
    s.bind(('::1', 5000))
    print("✅ Successfully bound to ::1")
    s.close()
except Exception as e:
    print(f"❌ Failed: {e}")
