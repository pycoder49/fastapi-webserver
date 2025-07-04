# fastapi-webserver
Building a web server using FastAPI in Python

For Ubuntu server deployment:
- Starting the service:
  - System services lie in: '/etc/systemd/system/'
  - Start command: `sudo systemctl start [service name excluding file extension]`
  - Observing status: `systemctl status [service name excluding extension]`
- Autmating start on boot/reboot
  - `sudo systemctl enable [service name without extension]`
  - When observing the status, you should now see 'enabled' at the top

In development
