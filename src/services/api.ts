const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ProjectData {
  name: string;
  description: string;
}

interface FileData {
  name: string;
  path: string;
  language: string;
  content: string;
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
}

export const api = {
  // Projects
  getProjects: async () => {
    const res = await fetch(`${API_URL}/api/projects/`);
    if (!res.ok) throw new Error('Failed to fetch projects');
    return res.json();
  },

  getProject: async (id: number) => {
    const res = await fetch(`${API_URL}/api/projects/${id}/`);
    if (!res.ok) throw new Error('Failed to fetch project');
    return res.json();
  },

  createProject: async (name: string, description: string) => {
    const res = await fetch(`${API_URL}/api/projects/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description }),
    });
    if (!res.ok) throw new Error('Failed to create project');
    return res.json();
  },

  updateProject: async (id: number, data: ProjectData) => {
    const res = await fetch(`${API_URL}/api/projects/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update project');
    return res.json();
  },

  deleteProject: async (id: number) => {
    const res = await fetch(`${API_URL}/api/projects/${id}/`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete project');
  },

  // Files
  getFiles: async (projectId: number) => {
    const res = await fetch(`${API_URL}/api/files/by_project/?project_id=${projectId}`);
    if (!res.ok) throw new Error('Failed to fetch files');
    return res.json();
  },

  getFile: async (id: number) => {
    const res = await fetch(`${API_URL}/api/files/${id}/`);
    if (!res.ok) throw new Error('Failed to fetch file');
    return res.json();
  },

  createFile: async (projectId: number, data: FileData) => {
    const res = await fetch(`${API_URL}/api/projects/${projectId}/create_file/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create file');
    return res.json();
  },

  updateFile: async (id: number, content: string) => {
    const res = await fetch(`${API_URL}/api/files/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
    });
    if (!res.ok) throw new Error('Failed to update file');
    return res.json();
  },

  deleteFile: async (id: number) => {
    const res = await fetch(`${API_URL}/api/files/${id}/`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete file');
  },

  executeFile: async (id: number) => {
    const res = await fetch(`${API_URL}/api/files/${id}/execute/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error('Failed to execute file');
    return res.json();
  },

  // Code Generation
  generateCode: async (projectId: number, prompt: string, language: string = 'python') => {
    const res = await fetch(`${API_URL}/api/generations/generate/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId, prompt, language }),
    });
    if (!res.ok) throw new Error('Failed to generate code');
    return res.json();
  },

  getGenerations: async (projectId: number) => {
    const res = await fetch(`${API_URL}/api/generations/by_project/?project_id=${projectId}`);
    if (!res.ok) throw new Error('Failed to fetch generations');
    return res.json();
  },
};
