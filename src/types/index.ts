export interface Project {
  id: number;
  name: string;
  description: string;
  files: File[];
  file_count: number;
  created_at: string;
  updated_at: string;
}

export interface File {
  id: number;
  name: string;
  path: string;
  content: string;
  language: string;
  created_at: string;
  updated_at: string;
}

export interface CodeGeneration {
  id: number;
  project: number;
  prompt: string;
  generated_code: string;
  language: string;
  model_used: string;
  created_at: string;
}

export interface ExecutionResult {
  id: number;
  file: number;
  language: string;
  stdout: string;
  stderr: string;
  exit_code: number;
  execution_time: number;
  created_at: string;
}

export interface Session {
  id: number;
  project: number;
  name: string;
  active_file: number | null;
  cursor_position: number;
  created_at: string;
  updated_at: string;
}
