import { ExecutionResult } from '../types';
import { X, Copy, Download } from 'lucide-react';

interface OutputPanelProps {
  result: ExecutionResult | null;
  isLoading?: boolean;
  onClose: () => void;
}

export function OutputPanel({ result, isLoading = false, onClose }: OutputPanelProps) {
  const hasOutput = result && (result.stdout || result.stderr);

  if (!hasOutput && !isLoading) {
    return null;
  }

  const handleCopy = () => {
    if (result) {
      const text = `${result.stdout}\n${result.stderr}`;
      navigator.clipboard.writeText(text);
    }
  };

  return (
    <div className="h-48 bg-slate-900 border-t border-slate-700 flex flex-col">
      <div className="border-b border-slate-700 p-3 flex items-center justify-between bg-slate-800">
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-slate-300">Output</span>
          {result && (
            <>
              <span
                className={`text-xs px-2 py-1 rounded ${
                  result.exit_code === 0
                    ? 'bg-emerald-900 text-emerald-200'
                    : 'bg-rose-900 text-rose-200'
                }`}
              >
                Exit Code: {result.exit_code}
              </span>
              <span className="text-xs text-slate-400">
                {result.execution_time.toFixed(2)}s
              </span>
            </>
          )}
        </div>
        <div className="flex items-center gap-2">
          {result && (
            <button
              onClick={handleCopy}
              className="p-2 hover:bg-slate-700 rounded transition-colors"
              title="Copy Output"
            >
              <Copy size={16} className="text-slate-400" />
            </button>
          )}
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-700 rounded transition-colors"
          >
            <X size={16} className="text-slate-400" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        <pre className="p-4 text-slate-300 text-xs font-mono whitespace-pre-wrap break-words">
          {isLoading ? (
            <span className="text-slate-500">Executing...</span>
          ) : (
            <>
              {result?.stdout && (
                <div>
                  <span className="text-emerald-400">$ Output:</span>
                  {'\n'}
                  {result.stdout}
                </div>
              )}
              {result?.stderr && (
                <div>
                  {result.stdout && '\n'}
                  <span className="text-rose-400">$ Errors:</span>
                  {'\n'}
                  {result.stderr}
                </div>
              )}
            </>
          )}
        </pre>
      </div>
    </div>
  );
}
