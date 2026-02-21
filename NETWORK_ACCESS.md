# 🌐 Accessing ZenStressy from Other Devices

## Quick Setup Guide

### Step 1: Start the Server
Run the application as normal:
```bash
python app.py
```

You'll see output like:
```
======================================================================
✅ ZenStressy Server Starting!
======================================================================
📱 Access on this device: http://localhost:5000
💻 Access on same network: http://192.168.1.100:5000
======================================================================

🔗 Share these URLs with devices on the same Wi-Fi network
⚠️  Make sure Windows Firewall allows Python on port 5000
======================================================================
```

### Step 2: Configure Windows Firewall

You have **3 options**:

#### Option A: Automatic Setup (Recommended)
1. Right-click on `allow_firewall.bat`
2. Select **"Run as Administrator"**
3. Follow the prompts
4. Done! ✅

#### Option B: Manual Setup
1. Open **Windows Firewall** settings
2. Click **"Allow an app through firewall"**
3. Click **"Change Settings"** (requires admin)
4. Find **Python** in the list
5. Check both **Private** and **Public** boxes
6. Click **OK**

#### Option C: Quick Port Allow
Open PowerShell as Administrator and run:
```powershell
netsh advfirewall firewall add rule name="ZenStressy" dir=in action=allow protocol=TCP localport=5000
```

### Step 3: Find Your IP Address

The server will automatically display your IP, but you can also:

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" under your Wi-Fi adapter

**Quick Check:**
```bash
python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print(s.getsockname()[0]); s.close()"
```

### Step 4: Access from Other Devices

#### On Your Laptop/Mobile:
1. Connect to the **same Wi-Fi network** as the server
2. Open browser
3. Enter: `http://YOUR_IP_ADDRESS:5000`
   - Example: `http://192.168.1.100:5000`

**That's it!** 🎉

## Troubleshooting

### ❌ "This site can't be reached"

**Check:**
1. Server is running on main computer
2. Both devices on same Wi-Fi
3. Firewall is configured
4. Using correct IP address

**Try:**
- Disable firewall temporarily to test
- Check Windows Defender isn't blocking
- Restart the server

### ❌ Connection Refused

**Solutions:**
1. Make sure server is running
2. Check the port (should be 5000)
3. Verify firewall allows Python

### ❌ "Connection timeout"

**Check:**
- Both devices on same network
- Correct IP address (not localhost)
- Firewall configured properly

### ❌ Can't find Python in Firewall

**Solution:**
Add port 5000 manually:
```powershell
netsh advfirewall firewall add rule name="Port 5000" dir=in action=allow protocol=TCP localport=5000
```

## Network Setup Tips

### For Home Network:
- Works automatically on most home routers
- All devices on same Wi-Fi can access

### For Office/School Network:
- May need IT approval
- Firewall rules might be stricter
- Consider VPN alternative

### For Mobile Hotspot:
- Enable mobile hotspot on your phone
- Connect both devices to hotspot
- Works great for testing!

## Security Notes

⚠️ **Important:**
- This setup is for **local network only**
- Server is **NOT exposed to the internet**
- Only devices on your Wi-Fi can access
- Debug mode is ON for development

🔒 **For Production:**
- Turn off debug mode
- Use proper authentication
- Consider HTTPS
- Use a reverse proxy (nginx)

## Quick Commands Reference

```bash
# Start server
python app.py

# Find your IP
ipconfig

# Add firewall rule (Admin PowerShell)
netsh advfirewall firewall add rule name="ZenStressy" dir=in action=allow protocol=TCP localport=5000

# Remove firewall rule
netsh advfirewall firewall delete rule name="ZenStressy"

# Check if port is open
netstat -an | findstr :5000
```

## Test Your Setup

### Test Checklist:
- [ ] Server starts without errors
- [ ] Localhost works (http://localhost:5000)
- [ ] Local IP works on same device
- [ ] Other device can access via IP
- [ ] Login works from other device
- [ ] Dashboard loads correctly
- [ ] Predictions work from other device

## Common IP Ranges

Your IP will typically look like:
- `192.168.1.xxx` (Most home routers)
- `192.168.0.xxx` (Alternative)
- `10.0.0.xxx` (Some networks)
- `172.16.xxx.xxx` (Corporate networks)

## Need Help?

If you're still having issues:
1. Make sure server console shows the correct IP
2. Check Windows Firewall logs
3. Try disabling antivirus temporarily
4. Ensure both devices on same Wi-Fi
5. Restart router if network issues

---

**Your server IP will be displayed when you start the app!**
Share that IP with other devices on your network! 🚀

