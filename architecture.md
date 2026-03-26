# Daily English Boost Telegram Bot
## Architecture & Major Requirements

### 1. Database Layer (Supabase / PostgreSQL)
- **Tool:** Supabase (PostgreSQL) with `supabase-py`.
- **Why:** Replaces the local SQLite database (`users.db`) to provide persistent storage. Free cloud hosting platforms often use ephemeral file systems that delete local files upon restart.
- **Schema:** 
  - Table: `users`
  - Columns:
    - `id_hash` (Text, Primary Key) - A deterministic SHA-256 hash of the Telegram ID.
    - `encrypted_id` (Text) - The user's Fernet-encrypted Telegram ID.
    - `level` (Text) - The chosen vocabulary level (A1, A2, B1, B2, C1, C2).

### 2. Security (User ID Encryption)
- **Tool:** `cryptography.fernet` (Symmetric encryption).
- **Why:** To completely mask the Telegram chat IDs of the bot's users from the database. Even if the Supabase database is compromised, the attackers will receive indistinguishable encrypted text, not the actual IDs.
- **Flow:** 
  - **Save:** Generate `id_hash(chat_id)` and `encrypt_id(chat_id)` -> Save to DB columns.
  - **Read:** Retrieve `encrypted_id` from DB -> `decrypt_id(encrypted_text)` -> Get back `chat_id` to send messages.
  - Required Environment Variable: `ENCRYPTION_KEY`

### 3. Application Layer (Telegram Bot)
- **Tool:** `python-telegram-bot`, `python-dotenv`.
- **Mode:** Long-Polling (`application.run_polling()`).
- **Core Loop:** Uses `JobQueue` to schedule a background task that pulls a word from `words.json` and broadcasts it to all users at 04:00 UTC daily.
- Required Environment Variable: `TOKEN`

### 4. Deployment Strategy (Render.com Free Tier)
- **Tool:** Render Web Service hook + Lightweight web server (`Flask` or `aiohttp`).
- **Why:** A "Background Worker" on Render costs money, but a "Web Service" is free. However, a Web Service *must* listen to web traffic on `$PORT`. If it does, Render keeps it alive. Free tier Web Services spin down after 15 minutes of inactivity.
- **Keep-alive Flow:**
  - A minimalist web server responds `200 OK` at `GET /`.
  - A free external cron job (e.g., UptimeRobot) pings this server every 10-14 minutes.
  - This prevents Render from putting the bot to sleep, allowing the Telegram polling mechanism and the `JobQueue` daily schedule to run uninterrupted 24/7 without cost.

### 5. Secrets Management (Environment Variables)
No secrets should ever be hardcoded. They are read from environment variables:
- `TOKEN`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `ENCRYPTION_KEY`
