const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  // Projects
  getProjects: async () => {
    const res = await fetch(`${API_URL}/api/projects/`);
    return res.json();
  },

  getProject: async (id: number) => {
    const res = await fetch(`${API_URL}/api/projects/${id}/`);
    return res.json();
  },

  createProject: async (name: string, description: string) => {
    const res = await fetch(`${API_URL}/api/projects/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description }),
    });
    return res.json();
  },

  updateProject: async (id: number, data: any) => {
    const res = await fetch(`${API_URL}/api/projects/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  deleteProject: async (id: number) => {
    await fetch(`${API_URL}/api/projects/${id}/`, { method: 'DELETE' });
  },

  // Files
  getFiles: async (projectId: number) => {
    const res = await fetch(`${API_URL}/api/files/by_project/?project_id=${projectId}`);
    return res.json();
  },

  getFile: async (id: number) => {
    const res = await fetch(`${API_URL}/api/files/${id}/`);
    return res.json();
  },

  createFile: async (projectId: number, data: any) => {
    const res = await fetch(`${API_URL}/api/projects/${projectId}/create_file/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  updateFile: async (id: number, content: string) => {
    const res = await fetch(`${API_URL}/api/files/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
    });
    return res.json();
  },

  deleteFile: async (id: number) => {
    await fetch(`${API_URL}/api/files/${id}/`, { method: 'DELETE' });
  },

  executeFile: async (id: number) => {
    const res = await fetch(`${API_URL}/api/files/${id}/execute/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    return res.json();
  },

  // Code Generation
  generateCode: async (projectId: number, prompt: string, language: string = 'python') => {
    const res = await fetch(`${API_URL}/api/generations/generate/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId, prompt, language }),
    });
    return res.json();
  },

  getGenerations: async (projectId: number) => {
    const res = await fetch(`${API_URL}/api/generations/by_project/?project_id=${projectId}`);
    return res.json();
  },
};
