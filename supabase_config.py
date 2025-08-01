from supabase import create_client, Client

SUPABASE_URL = "https://jamuzjjhjpotnxttzkyf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImphbXV6ampoanBvdG54dHR6a3lmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQwMTk2MTUsImV4cCI6MjA2OTU5NTYxNX0.us0ULhKQGRpDOZ6mF1vVolcAhGdKD0urycJabMzt8qQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)