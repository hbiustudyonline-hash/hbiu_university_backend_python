# 🚀 Railway Deployment Guide for HBIU Python Backend

## Quick Railway Deployment

### Step 1: Railway Setup
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub account
3. Create new project: "Deploy from GitHub repo"
4. Select repository: `hbiu_university_backend_python`
5. Railway will auto-detect Python and start deployment

### Step 2: Environment Variables
Add these in Railway Dashboard → Variables:

**Required:**
```
SECRET_KEY=your-super-secret-jwt-key-here-minimum-32-characters-long
```

**Optional (for AI features):**
```
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

**Database (if using PostgreSQL):**
```
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Step 3: Verify Deployment

1. **Check deployment logs** in Railway dashboard
2. **Test health endpoint**: `https://your-app.railway.app/`
3. **Check API docs**: `https://your-app.railway.app/docs`

### Step 4: Frontend Integration

Update your frontend API base URL to point to Railway:
```javascript
const API_BASE_URL = 'https://your-app.railway.app';
```

## Expected Railway URLs

Your app will be available at:
- **API**: `https://[random-name].railway.app`
- **Docs**: `https://[random-name].railway.app/docs`
- **Health**: `https://[random-name].railway.app/`

## Deployment Features

✅ **Auto-deployment** from GitHub pushes
✅ **Health checks** on root endpoint
✅ **Environment variables** support
✅ **Automatic HTTPS** 
✅ **Custom domains** support
✅ **Logs and monitoring**

## Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app.railway.app/
```
Expected: `{"message":"HBIU University Backend API","status":"running"}`

### 2. Authentication Test
```bash
curl -X POST https://your-app.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 3. AI Capabilities Test
```bash
# Replace TOKEN with token from login response
curl -H "Authorization: Bearer TOKEN" \
  https://your-app.railway.app/api/ai/capabilities
```

## Troubleshooting

### Common Issues:

**1. Deployment Failed**
- Check Railway logs for Python/pip errors
- Verify `requirements.txt` is correct
- Ensure `Procfile` exists

**2. 500 Internal Server Error**
- Check environment variables are set
- Review application logs in Railway dashboard
- Verify SECRET_KEY is set and sufficiently long

**3. CORS Issues**
- Ensure frontend URL is in CORS origins
- Check Railway app URL is correct
- Update frontend API configuration

**4. AI Features Not Working**
- Verify OPENAI_API_KEY is set correctly
- Check OpenAI API quota and billing
- AI will gracefully degrade without API key

### Build Configuration

Railway uses these files:
- `Procfile` - Start command
- `railway.json` - Deploy configuration  
- `nixpacks.toml` - Build configuration
- `requirements.txt` - Python dependencies

## Next Steps

1. **Custom Domain**: Add your own domain in Railway settings
2. **Database**: Add PostgreSQL service if needed
3. **Monitoring**: Set up alerts and monitoring
4. **Scaling**: Configure auto-scaling based on usage

## Support

- **Railway Docs**: https://docs.railway.app
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **OpenAI API**: https://platform.openai.com/docs

---

Your Python FastAPI backend is now ready for production! 🎉