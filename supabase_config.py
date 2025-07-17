from supabase import create_client, Client

SUPABASE_URL = "https://imxesrkdgciojihloufi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlteGVzcmtkZ2Npb2ppaGxvdWZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE1MTUwOTksImV4cCI6MjA2NzA5MTA5OX0.TUadZdOTfE9BscVpxOFYKbjenjqPfVz0R7i21ebCwQ8"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)