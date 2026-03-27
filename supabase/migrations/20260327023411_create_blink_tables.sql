/*
  # Create Blink Core Tables

  1. New Tables
    - `projects`
      - `id` (uuid, primary key)
      - `name` (text)
      - `description` (text)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    
    - `files`
      - `id` (uuid, primary key)
      - `project_id` (uuid, foreign key)
      - `name` (text)
      - `path` (text)
      - `content` (text)
      - `language` (text)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    
    - `code_generations`
      - `id` (uuid, primary key)
      - `project_id` (uuid, foreign key)
      - `prompt` (text)
      - `generated_code` (text)
      - `language` (text)
      - `model_used` (text)
      - `created_at` (timestamptz)
    
    - `execution_results`
      - `id` (uuid, primary key)
      - `file_id` (uuid, foreign key)
      - `language` (text)
      - `stdout` (text)
      - `stderr` (text)
      - `exit_code` (int)
      - `execution_time` (float)
      - `created_at` (timestamptz)
    
    - `sessions`
      - `id` (uuid, primary key)
      - `project_id` (uuid, foreign key)
      - `name` (text)
      - `active_file_id` (uuid, foreign key, nullable)
      - `cursor_position` (int)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)

  2. Security
    - Enable RLS on all tables
    - Add policies allowing all authenticated operations for now (can be restricted per user later)

  3. Indexes
    - Add indexes on frequently queried columns
*/

CREATE TABLE IF NOT EXISTS projects (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS files (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  name text NOT NULL,
  path text NOT NULL,
  content text DEFAULT '',
  language text DEFAULT 'text',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(project_id, path)
);

CREATE TABLE IF NOT EXISTS code_generations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  prompt text NOT NULL,
  generated_code text NOT NULL,
  language text DEFAULT 'python',
  model_used text DEFAULT 'codellama',
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS execution_results (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  file_id uuid NOT NULL REFERENCES files(id) ON DELETE CASCADE,
  language text NOT NULL,
  stdout text DEFAULT '',
  stderr text DEFAULT '',
  exit_code integer DEFAULT 0,
  execution_time float DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  name text NOT NULL,
  active_file_id uuid REFERENCES files(id) ON DELETE SET NULL,
  cursor_position integer DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE files ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_generations ENABLE ROW LEVEL SECURITY;
ALTER TABLE execution_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations on projects" ON projects FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on files" ON files FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on code_generations" ON code_generations FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on execution_results" ON execution_results FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on sessions" ON sessions FOR ALL USING (true) WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_files_project_id ON files(project_id);
CREATE INDEX IF NOT EXISTS idx_files_language ON files(language);
CREATE INDEX IF NOT EXISTS idx_code_generations_project_id ON code_generations(project_id);
CREATE INDEX IF NOT EXISTS idx_execution_results_file_id ON execution_results(file_id);
CREATE INDEX IF NOT EXISTS idx_sessions_project_id ON sessions(project_id);
