-- Supabase SQL Editor mein ye pura script ek baar run karein

-- Table 1: Auto-posted channel content ka duplicate-check record
create table posted_content (
  id bigint generated always as identity primary key,
  content_hash text unique not null,
  title text,
  content_type text,
  posted_at timestamptz default now()
);

create index idx_content_hash on posted_content (content_hash);

-- Table 2: Agent ki conversation history (memory ke liye)
create table chat_history (
  id bigint generated always as identity primary key,
  chat_id text not null,
  role text not null,       -- 'user' ya 'assistant'
  content text,
  created_at timestamptz default now()
);

create index idx_chat_id on chat_history (chat_id, created_at);
