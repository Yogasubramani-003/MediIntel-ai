# MediIntel AI - Quick Reference

## 🚀 Start the Application

### Windows
```bash
quick-start.bat
```

### macOS/Linux
```bash
chmod +x quick-start.sh
./quick-start.sh
```

### Manual Start
```bash
docker compose up --build
```

---

## 🌐 Access Points

| Service | URL |
|---------|-----|
| Web Application | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Database | localhost:5432 |

---

## 🛑 Common Commands

### Stop Application
```bash
docker compose down
```

### View Logs
```bash
docker compose logs -f
```

### Restart Services
```bash
docker compose restart
```

### Clean Everything (Remove Volumes)
```bash
docker compose down -v
```

### Rebuild from Scratch
```bash
docker compose down -v
docker compose build --no-cache
docker compose up
```

---

## 📊 API Endpoints

### Upload Document
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@medical_document.pdf"
```

### Get Patient Data
```bash
curl http://localhost:8000/patient/1
```

### Chat with AI
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"patient_id": 1, "question": "What medications?"}'
```

---

## 🐛 Quick Troubleshooting

### Port 8000 Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Database Connection Failed
```bash
# Check if PostgreSQL container is running
docker compose ps

# Restart database
docker compose restart db
```

### Cannot Access Application
1. Check if Docker is running
2. Verify containers are up: `docker compose ps`
3. Check logs: `docker compose logs web`
4. Ensure port 8000 is not blocked by firewall

### Docker Build Failed
```bash
# Clean and rebuild
docker compose down -v
docker system prune -af
docker compose up --build
```

---

## 📁 File Locations

### Uploaded Files
- **Docker:** Inside container at `/app/uploads`
- **Local:** `./uploads` directory

### Logs
```bash
docker compose logs web    # Application logs
docker compose logs db     # Database logs
```

### Database Data
- **Docker Volume:** `postgres_data`
- **View:** `docker volume inspect mediintel-ai_postgres_data`

---

## 🔧 Environment Variables

### Default Values
```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/mediintel
UPLOAD_FOLDER=/app/uploads
DEBUG=False
```

### Change Database Password
Edit `docker-compose.yml`:
```yaml
environment:
  POSTGRES_PASSWORD: your_secure_password
```

---

## 📦 System Requirements

### Minimum
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Disk:** 10 GB free space
- **Docker:** 20.10+
- **Docker Compose:** 2.0+

### Recommended
- **CPU:** 4+ cores
- **RAM:** 8+ GB
- **Disk:** 20+ GB SSD

---

## 🎯 Testing Checklist

- [ ] Application starts without errors
- [ ] Can access http://localhost:8000
- [ ] Upload page loads correctly
- [ ] Can drag and drop files
- [ ] File upload completes successfully
- [ ] Dashboard shows extracted data
- [ ] Charts render properly
- [ ] AI chat responds to questions

---

## 🔑 Default Credentials

### PostgreSQL
- **User:** postgres
- **Password:** postgres
- **Database:** mediintel
- **Port:** 5432

⚠️ **Change these for production!**

---

## 📞 Need Help?

1. **Check logs:** `docker compose logs -f`
2. **Read setup guide:** See `SETUP_GUIDE.md`
3. **Review fixes:** See `FIXES_APPLIED.md`
4. **Verify Docker:** `docker --version`
5. **Check containers:** `docker compose ps`

---

## 🎨 Supported File Types

- **Documents:** PDF
- **Images:** JPG, JPEG, PNG
- **Content:** Medical records, prescriptions, lab reports, discharge summaries

---

## ⚡ Quick Performance Tips

1. Use SSD for Docker storage
2. Allocate at least 4GB RAM to Docker
3. Use PDF at 200+ DPI for better OCR
4. Keep uploaded files under 10MB
5. Clean old uploads periodically

---

## 🔄 Update Application

```bash
# Pull latest changes (if using git)
git pull

# Rebuild and restart
docker compose down
docker compose up --build
```

---

## 💾 Backup Data

### Backup Database
```bash
docker compose exec db pg_dump -U postgres mediintel > backup.sql
```

### Restore Database
```bash
docker compose exec -T db psql -U postgres mediintel < backup.sql
```

### Backup Uploads
```bash
docker compose cp web:/app/uploads ./backup_uploads
```

---

## ✅ Health Checks

### Check Application Health
```bash
curl http://localhost:8000/
```

### Check Database Connection
```bash
docker compose exec db psql -U postgres -d mediintel -c "SELECT 1"
```

### Check Docker Status
```bash
docker compose ps
docker stats
```

---

## 🚨 Emergency Commands

### Stop Everything Immediately
```bash
docker compose kill
```

### Remove All Containers and Data
```bash
docker compose down -v
docker system prune -af --volumes
```

### Restart Docker (if stuck)
```bash
# Windows/macOS: Restart Docker Desktop
# Linux:
sudo systemctl restart docker
```

---

## 📈 Monitor Resources

### View Resource Usage
```bash
docker stats
```

### Check Disk Usage
```bash
docker system df
```

### Clean Up Unused Resources
```bash
docker system prune -a
```

---

**Last Updated:** 2024
**Version:** 1.0
**Status:** ✅ All systems operational
