import { File as FileType, Project } from '../types';
import { ChevronRight, File, Plus, Trash2 } from 'lucide-react';
import { useState } from 'react';

interface FileTreeProps {
  project: Project | null;
  selectedFile: FileType | null;
  onSelectFile: (file: FileType) => void;
  onCreateFile: () => void;
  onDeleteFile: (fileId: number) => void;
}

export function FileTree({
  project,
  selectedFile,
  onSelectFile,
  onCreateFile,
  onDeleteFile,
}: FileTreeProps) {
  const [expanded, setExpanded] = useState(true);

  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  if (!project) {
    return (
      <div className="w-64 bg-slate-800 border-r border-slate-700 p-4 text-slate-400">
        <p className="text-sm">No project selected</p>
      </div>
    );
  }

  return (
    <div className="w-64 bg-slate-800 border-r border-slate-700 overflow-y-auto flex flex-col">
      <div className="p-4 border-b border-slate-700">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={toggleExpanded}
            className="flex items-center gap-2 text-slate-300 hover:text-slate-100 font-semibold"
          >
            <ChevronRight size={16} className={`transition-transform ${expanded ? 'rotate-90' : ''}`} />
            {project.name}
          </button>
          <button
            onClick={onCreateFile}
            className="p-1 hover:bg-slate-700 rounded transition-colors"
            title="New File"
          >
            <Plus size={16} className="text-slate-400" />
          </button>
        </div>
      </div>

      {expanded && (
        <div className="flex-1 overflow-y-auto">
          {project.files && project.files.length > 0 ? (
            <div className="p-2">
              {project.files.map((file) => (
                <div
                  key={file.id}
                  onClick={() => onSelectFile(file)}
                  className={`flex items-center justify-between p-2 rounded text-sm cursor-pointer transition-colors ${
                    selectedFile?.id === file.id
                      ? 'bg-slate-700 text-slate-100'
                      : 'text-slate-400 hover:bg-slate-700'
                  }`}
                >
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <File size={14} className="flex-shrink-0" />
                    <span className="truncate">{file.name}</span>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteFile(file.id);
                    }}
                    className="p-1 hover:text-rose-400 opacity-0 hover:opacity-100 transition-all"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-4 text-sm text-slate-500">
              <p>No files yet</p>
              <p className="text-xs mt-2">Click the + button to create one</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
