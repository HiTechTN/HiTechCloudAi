import { useState, useEffect } from 'react';
import { File as FileType, Project, CodeGeneration, ExecutionResult } from './types';
import { api } from './services/api';
import { FileTree } from './components/FileTree';
import { Editor } from './components/Editor';
import { OutputPanel } from './components/OutputPanel';
import { AIPanel } from './components/AIPanel';
import { Plus, Settings } from 'lucide-react';

function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [selectedFile, setSelectedFile] = useState<FileType | null>(null);
  const [executionResult, setExecutionResult] = useState<ExecutionResult | null>(null);
  const [generations, setGenerations] = useState<CodeGeneration[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');

  useEffect(() => {
    loadProjects();
  }, []);

  useEffect(() => {
    if (selectedProject) {
      loadGenerations();
    }
  }, [selectedProject]);

  const loadProjects = async () => {
    try {
      const data = await api.getProjects();
      setProjects(data);
      if (data.length > 0 && !selectedProject) {
        setSelectedProject(data[0]);
      }
    } catch (error) {
      console.error('Failed to load projects:', error);
    }
  };

  const loadGenerations = async () => {
    if (!selectedProject) return;
    try {
      const data = await api.getGenerations(selectedProject.id);
      setGenerations(data);
    } catch (error) {
      console.error('Failed to load generations:', error);
    }
  };

  const createProject = async () => {
    if (!newProjectName.trim()) return;
    try {
      const project = await api.createProject(newProjectName, '');
      setProjects([...projects, project]);
      setSelectedProject(project);
      setNewProjectName('');
      setShowNewProjectModal(false);
    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  const createFile = async () => {
    if (!selectedProject) return;
    try {
      const file = await api.createFile(selectedProject.id, {
        name: 'untitled.py',
        path: `untitled_${Date.now()}.py`,
        language: 'python',
        content: '',
      });
      setSelectedProject({
        ...selectedProject,
        files: [...(selectedProject.files || []), file],
      });
      setSelectedFile(file);
    } catch (error) {
      console.error('Failed to create file:', error);
    }
  };

  const saveFile = async (content: string) => {
    if (!selectedFile) return;
    try {
      const updated = await api.updateFile(selectedFile.id, content);
      setSelectedFile(updated);
      if (selectedProject) {
        setSelectedProject({
          ...selectedProject,
          files: selectedProject.files.map((f) => (f.id === updated.id ? updated : f)),
        });
      }
    } catch (error) {
      console.error('Failed to save file:', error);
    }
  };

  const executeFile = async () => {
    if (!selectedFile) return;
    setIsLoading(true);
    try {
      const result = await api.executeFile(selectedFile.id);
      setExecutionResult(result);
    } catch (error) {
      console.error('Failed to execute file:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteFile = async () => {
    if (!selectedFile) return;
    try {
      await api.deleteFile(selectedFile.id);
      if (selectedProject) {
        setSelectedProject({
          ...selectedProject,
          files: selectedProject.files.filter((f) => f.id !== selectedFile.id),
        });
      }
      setSelectedFile(null);
    } catch (error) {
      console.error('Failed to delete file:', error);
    }
  };

  const generateCode = async (prompt: string, language: string) => {
    if (!selectedProject) return;
    setIsLoading(true);
    try {
      const generation = await api.generateCode(selectedProject.id, prompt, language);
      setGenerations([generation, ...generations]);
    } catch (error) {
      console.error('Failed to generate code:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const insertCode = (code: string) => {
    if (selectedFile) {
      const newContent = selectedFile.content + '\n' + code;
      setSelectedFile({ ...selectedFile, content: newContent });
    }
  };

  return (
    <div className="h-screen bg-slate-900 flex flex-col text-slate-100">
      <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold text-white">Blink.local</h1>
          <div className="flex items-center gap-2 bg-slate-700 rounded-lg px-3 py-1">
            {selectedProject ? (
              <>
                <span className="text-sm text-slate-300">{selectedProject.name}</span>
                <button
                  onClick={() => setShowNewProjectModal(true)}
                  className="ml-2 p-1 hover:bg-slate-600 rounded transition-colors"
                >
                  <Plus size={14} />
                </button>
              </>
            ) : (
              <button
                onClick={() => setShowNewProjectModal(true)}
                className="flex items-center gap-1 text-sm text-slate-400 hover:text-slate-300"
              >
                <Plus size={14} />
                New Project
              </button>
            )}
          </div>
        </div>
        <button className="p-2 hover:bg-slate-700 rounded transition-colors">
          <Settings size={20} />
        </button>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <FileTree
          project={selectedProject}
          selectedFile={selectedFile}
          onSelectFile={setSelectedFile}
          onCreateFile={createFile}
          onDeleteFile={deleteFile}
        />

        <Editor
          file={selectedFile}
          onSave={saveFile}
          onExecute={executeFile}
          onDelete={deleteFile}
          isLoading={isLoading}
        />

        <AIPanel
          generations={generations}
          onGenerate={generateCode}
          onInsertCode={insertCode}
          isLoading={isLoading}
        />
      </div>

      <OutputPanel result={executionResult} isLoading={isLoading} onClose={() => setExecutionResult(null)} />

      {showNewProjectModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-slate-800 rounded-lg p-6 w-96 border border-slate-700">
            <h2 className="text-lg font-semibold mb-4">New Project</h2>
            <input
              type="text"
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
              placeholder="Project name"
              className="w-full bg-slate-700 text-slate-100 px-3 py-2 rounded border border-slate-600 outline-none focus:border-blue-500 mb-4"
              onKeyPress={(e) => e.key === 'Enter' && createProject()}
            />
            <div className="flex gap-2">
              <button
                onClick={createProject}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded transition-colors"
              >
                Create
              </button>
              <button
                onClick={() => setShowNewProjectModal(false)}
                className="flex-1 bg-slate-700 hover:bg-slate-600 text-slate-200 py-2 rounded transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
