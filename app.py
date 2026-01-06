#!/usr/bin/env python3
"""
FastAGI Server - Replacing Actualize AI
Listens on port 4573 for calls from Asterisk
"""
import socket
import sys
import time
import os

print("FastAGI Server - Replacing Actualize AI\n")


# AGI SERVER CONFIGURATION
AGI_HOST = '0.0.0.0'  # Listen on all interfaces
AGI_PORT = int(os.environ.get('PORT', 4573))  # Use Render's PORT or default to 4573


def handle_incoming_call(client_socket):
    """Handle incoming call from Asterisk"""
    print("\n" + "="*60)
    print("INCOMING CALL FROM ASTERISK!")
    print("="*60)
    sys.stdout.flush()
    
    try:
        # Create file-like object for easier reading
        sock_file = client_socket.makefile('rw')
        
        # Read AGI environment variables
        env = {}
        print("Reading AGI environment...")
        while True:
            line = sock_file.readline().strip()
            print(f"   ENV: {line}")
            if not line:
                break
            if ":" in line:
                key, value = line.split(":", 1)
                env[key.strip()] = value.strip()
        
        caller = env.get("agi_callerid", "Unknown")
        channel = env.get("agi_channel", "Unknown")
        
        print(f"Caller: {caller}")
        print(f"Channel: {channel}")
        sys.stdout.flush()
        
        # Answer the call
        print("Sending ANSWER command...")
        sock_file.write("ANSWER\n")
        sock_file.flush()
        response = sock_file.readline().strip()
        print(f"   <- Response: {response}")
        
        if "200" in response:
            print("Call answered successfully!")
        else:
            print(f"Unexpected response: {response}")
        sys.stdout.flush()
        
        # Keep call alive for 15 seconds
        print("Keeping call alive for 15 seconds...")
        sys.stdout.flush()
        
        for i in range(15):
            time.sleep(1)
            print(f"   {i+1}/15 seconds...", end='\r')
            sys.stdout.flush()
        
        print("\nSending HANGUP command...")
        sock_file.write("HANGUP\n")
        sock_file.flush()
        response = sock_file.readline().strip()
        print(f"   <- Response: {response}")
        print("Call ended")
        print("="*60 + "\n")
        sys.stdout.flush()
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
    finally:
        try:
            sock_file.close()
            client_socket.close()
        except:
            pass

# ============================================
# START FASTAGI SERVER
# ============================================

print(f"Starting FastAGI Server...")
print(f"   Listening on: {AGI_HOST}:{AGI_PORT}")
print(f"   Asterisk will connect to: 102.176.75.169:{AGI_PORT}\n")
sys.stdout.flush()

try:
    # Create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((AGI_HOST, AGI_PORT))
    server.listen(5)
    
    print("="*60)
    print(f"FastAGI Server READY on port {AGI_PORT}")
    print("="*60)
    print("\nDialplan configured for: 0596921958")
    print("Call that number to test!")
    print("Press Ctrl+C to stop\n")
    sys.stdout.flush()
    
    # Accept incoming connections from Asterisk
    while True:
        print("Waiting for call from Asterisk...")
        sys.stdout.flush()
        
        client_socket, client_address = server.accept()
        print(f"Connected: {client_address}")
        sys.stdout.flush()
        
        # Handle the call
        handle_incoming_call(client_socket)
        
except KeyboardInterrupt:
    print("\n\nStopping FastAGI Server...")
    server.close()
    print("Done")
    
except Exception as e:
    print(f"\nServer error: {e}")
    import traceback
    traceback.print_exc()