import { useState } from 'react';
import { Send, Copy, Trash2, ChevronDown } from 'lucide-react';
import { CodeGeneration } from '../types';

interface AIPanelProps {
  generations: CodeGeneration[];
  onGenerate: (prompt: string, language: string) => void;
  onInsertCode: (code: string) => void;
  isLoading?: boolean;
}

export function AIPanel({ generations, onGenerate, onInsertCode, isLoading = false }: AIPanelProps) {
  const [prompt, setPrompt] = useState('');
  const [language, setLanguage] = useState('python');
  const [expanded, setExpanded] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      onGenerate(prompt, language);
      setPrompt('');
    }
  };

  const handleCopy = (code: string) => {
    navigator.clipboard.writeText(code);
  };

  return (
    <div className="w-96 bg-slate-800 border-l border-slate-700 flex flex-col overflow-hidden">
      <div className="border-b border-slate-700 p-4 flex items-center justify-between bg-slate-800">
        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center gap-2 text-slate-300 hover:text-slate-100 font-semibold"
        >
          <ChevronDown size={16} className={`transition-transform ${expanded ? '' : '-rotate-90'}`} />
          AI Code Assistant
        </button>
      </div>

      {expanded && (
        <>
          <div className="border-b border-slate-700 p-4">
            <form onSubmit={handleSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Language</label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full bg-slate-700 text-slate-100 text-sm rounded px-2 py-1 border border-slate-600 outline-none focus:border-blue-500"
                >
                  <option>python</option>
                  <option>javascript</option>
                  <option>typescript</option>
                  <option>bash</option>
                  <option>go</option>
                  <option>rust</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Prompt</label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe the code you want to generate..."
                  className="w-full bg-slate-700 text-slate-100 text-sm rounded px-2 py-2 border border-slate-600 outline-none focus:border-blue-500 resize-none"
                  rows={3}
                />
              </div>

              <button
                type="submit"
                disabled={isLoading || !prompt.trim()}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 text-white text-sm font-medium py-2 rounded flex items-center justify-center gap-2 transition-colors"
              >
                <Send size={14} />
                Generate
              </button>
            </form>
          </div>

          <div className="flex-1 overflow-y-auto space-y-2 p-4">
            {generations.length === 0 ? (
              <p className="text-sm text-slate-500">No generations yet</p>
            ) : (
              generations.map((gen) => (
                <div
                  key={gen.id}
                  className="bg-slate-700 rounded p-3 space-y-2 text-sm border border-slate-600"
                >
                  <div className="flex items-start justify-between gap-2">
                    <p className="text-slate-300">{gen.prompt}</p>
                    <span className="text-xs text-slate-400 whitespace-nowrap">{gen.language}</span>
                  </div>
                  <pre className="bg-slate-600 p-2 rounded text-xs text-slate-200 overflow-x-auto max-h-24">
                    {gen.generated_code}
                  </pre>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleCopy(gen.generated_code)}
                      className="flex-1 flex items-center justify-center gap-1 bg-slate-600 hover:bg-slate-500 text-slate-200 text-xs py-1 rounded transition-colors"
                    >
                      <Copy size={12} />
                      Copy
                    </button>
                    <button
                      onClick={() => onInsertCode(gen.generated_code)}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-xs py-1 rounded transition-colors"
                    >
                      Insert
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}
