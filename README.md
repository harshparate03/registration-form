# Registration Form (Flask + Neon)

A Bootstrap registration form served by Flask. Submissions are validated on the server and stored in Neon PostgreSQL. Passwords are stored as salted PBKDF2-SHA256 hashes. The selected image is limited to 5 MB and stored in PostgreSQL as `BYTEA`.

## Run locally

1. Create a Neon project and copy its pooled connection string.
2. Copy `.env.example` to `.env` and replace the example URL. Do not commit `.env`.
3. In PowerShell, set the connection for the current terminal:

   ```powershell
   $env:DATABASE_URL='YOUR_NEON_POOLED_CONNECTION_STRING'
   ```

4. Install and run:

   ```powershell
   python -m pip install -r requirements.txt
   python app.py
   ```

5. Open `http://localhost:8000`.

The `registrations` table is created automatically. `schema.sql` is also provided for manual creation in the Neon SQL Editor.

## Push to GitHub

Create an empty repository on GitHub, then run:

```powershell
git init
git add .
git commit -m "Deploy Flask registration form with Neon"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

## Deploy from GitHub on Render

1. In Render, select **New > Blueprint**.
2. Connect the GitHub repository.
3. Render reads `render.yaml` from the repository root.
4. When prompted for `DATABASE_URL`, paste the pooled Neon connection string.
5. Create the Blueprint and wait for the deployment.
6. Open the generated `.onrender.com` URL.

Do not deploy this application with GitHub Pages. Pages is static hosting and cannot run the Flask backend.