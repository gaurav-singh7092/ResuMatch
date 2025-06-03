import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, Check, AlertCircle } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  acceptedTypes: string[];
  maxSize: number;
  title: string;
  description: string;
  className?: string;
  multiple?: boolean;
  uploadedFiles?: File[];
}

export default function FileUpload({
  onFileSelect,
  acceptedTypes,
  maxSize,
  title,
  description,
  className = '',
  multiple = false,
  uploadedFiles = [],
}: FileUploadProps) {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(
    async (acceptedFiles: File[], rejectedFiles: any[]) => {
      if (rejectedFiles.length > 0) {
        const error = rejectedFiles[0].errors[0];
        if (error.code === 'file-too-large') {
          toast.error(`File is too large. Maximum size is ${maxSize / 1024 / 1024}MB`);
        } else if (error.code === 'file-invalid-type') {
          toast.error('Invalid file type. Please upload a supported format.');
        } else {
          toast.error('File upload failed. Please try again.');
        }
        return;
      }

      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        setIsUploading(true);
        
        setTimeout(() => {
          setUploadedFile(file);
          setIsUploading(false);
          onFileSelect(file);
          toast.success('File uploaded successfully!');
        }, 1500);
      }
    },
    [onFileSelect, maxSize]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedTypes.reduce((acc, type) => ({ ...acc, [type]: [] }), {}),
    maxSize,
    multiple: false,
  });

  const removeFile = () => {
    setUploadedFile(null);
    toast.success('File removed');
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className={`w-full min-h-[280px] md:min-h-[320px] ${className}`}>
      {!uploadedFile ? (
        <div
          {...getRootProps()}
          className={`
            relative border-2 border-dashed rounded-2xl p-6 md:p-8 text-center cursor-pointer transition-all duration-300 h-full min-h-[280px] md:min-h-[320px] flex items-center justify-center
            ${isDragActive 
              ? 'border-primary-500 bg-primary-50 scale-105' 
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }
            ${isUploading ? 'pointer-events-none opacity-50' : ''}
          `}
        >
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center space-y-4">
            <div
              className={`
                w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-200
                ${isDragActive 
                  ? 'bg-primary-500 text-white' 
                  : 'bg-gray-100 text-gray-600'
                }
              `}
            >
              {isUploading ? (
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Upload className="w-8 h-8" />
              )}
            </div>

            <div className="space-y-2">
              <h3 className="text-lg font-semibold text-gray-900">
                {isUploading ? 'Uploading...' : title}
              </h3>
              <p className="text-sm text-gray-600 max-w-xs">
                {isUploading ? 'Please wait while we process your file' : description}
              </p>
              {!isUploading && (
                <div className="text-xs text-gray-500 mt-2">
                  <p>Max file size: {Math.round(maxSize / 1024 / 1024)}MB</p>
                  <p>Supported: {acceptedTypes.join(', ')}</p>
                </div>
              )}
            </div>

            {isDragActive && (
              <div className="absolute inset-0 rounded-2xl bg-primary-50 border-2 border-primary-500 flex items-center justify-center">
                <p className="text-primary-600 font-medium">Drop your file here!</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-gray-200 p-4 md:p-6 shadow-sm min-h-[280px] md:min-h-[320px] flex items-center">
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <Check className="w-6 h-6 text-green-600" />
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium text-gray-900 truncate">
                  {uploadedFile.name}
                </h4>
                <p className="text-sm text-gray-600">
                  {formatFileSize(uploadedFile.size)}
                </p>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
              title="Remove file"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      {multiple && uploadedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          <h4 className="text-sm font-medium text-gray-900">
            Uploaded Files ({uploadedFiles.length})
          </h4>
          <div className="space-y-2">
            {uploadedFiles.map((file, index) => (
              <div
                key={`${file.name}-${index}`}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <File className="w-5 h-5 text-gray-400" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{file.name}</p>
                    <p className="text-xs text-gray-600">{formatFileSize(file.size)}</p>
                  </div>
                </div>
                <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                  <Check className="w-3 h-3 text-green-600" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
