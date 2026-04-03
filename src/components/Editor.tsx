import { useState, useEffect } from 'react';
import { File as FileType } from '../types';
import { Save, Play, Copy, Trash2 } from 'lucide-react';

interface EditorProps {
  file: FileType | null;
  onSave: (content: string) => void;
  onExecute: () => void;
  onDelete: () => void;
  isLoading?: boolean;
}

export function Editor({ file, onSave, onExecute, onDelete, isLoading = false }: EditorProps) {
  const [content, setContent] = useState('');
  const [isSaved, setIsSaved] = useState(true);

  useEffect(() => {
    if (file) {
      setContent(file.content);
      setIsSaved(true);
    } else {
      setContent('');
    }
  }, [file]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value);
    setIsSaved(false);
  };

  const handleSave = () => {
    onSave(content);
    setIsSaved(true);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
  };

  if (!file) {
    return (
      <div className="flex-1 flex items-center justify-center bg-slate-900 text-slate-400">
        <p>Select or create a file to start editing</p>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-slate-900 border-l border-slate-700">
      <div className="border-b border-slate-700 p-4 flex items-center justify-between bg-slate-800">
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-slate-300">{file.name}</span>
          <span className="text-xs text-slate-500 bg-slate-700 px-2 py-1 rounded">
            {file.language}
          </span>
          {!isSaved && <span className="text-xs text-amber-500">●</span>}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="p-2 hover:bg-slate-700 rounded transition-colors"
            title="Copy"
          >
            <Copy size={16} className="text-slate-400" />
          </button>
          <button
            onClick={handleSave}
            disabled={isLoading}
            className="p-2 hover:bg-slate-700 rounded transition-colors disabled:opacity-50"
            title="Save"
          >
            <Save size={16} className="text-slate-400" />
          </button>
          <button
            onClick={onExecute}
            disabled={isLoading}
            className="p-2 hover:bg-emerald-600 rounded transition-colors disabled:opacity-50"
            title="Execute"
          >
            <Play size={16} className="text-emerald-400" />
          </button>
          <button
            onClick={onDelete}
            className="p-2 hover:bg-rose-600 rounded transition-colors"
            title="Delete"
          >
            <Trash2 size={16} className="text-rose-400" />
          </button>
        </div>
      </div>

      <textarea
        value={content}
        onChange={handleChange}
        className="flex-1 bg-slate-900 text-slate-100 p-4 font-mono text-sm resize-none outline-none"
        spellCheck="false"
      />
    </div>
  );
}
