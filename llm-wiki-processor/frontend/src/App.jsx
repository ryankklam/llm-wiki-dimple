import React, { useState } from 'react'
import './App.css'

function App() {
  const [videoUrl, setVideoUrl] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [status, setStatus] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [isValid, setIsValid] = useState(true)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // 表单验证
    if (!videoUrl) {
      setError('请输入小红书视频链接')
      setIsValid(false)
      return
    }

    // 验证链接格式
    if (!videoUrl.includes('xiaohongshu.com') && !videoUrl.includes('xhslink.com')) {
      setError('请输入有效的小红书视频链接')
      setIsValid(false)
      return
    }

    setIsProcessing(true)
    setStatus('正在处理视频...')
    setError('')
    setIsValid(true)
    setResult(null)

    try {
      const response = await fetch('http://localhost:3001/api/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_url: videoUrl })
      })

      const data = await response.json()
      
      if (data.status === 'success') {
        setStatus('处理成功')
        setResult(data)
      } else {
        throw new Error(data.error || '处理失败')
      }
    } catch (err) {
      setStatus('处理失败')
      setError(err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleInputChange = (e) => {
    setVideoUrl(e.target.value)
    if (error) {
      setError('')
      setIsValid(true)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-3xl bg-white rounded-xl shadow-lg p-6 md:p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
            LLM Wiki Processor
          </h1>
          <p className="text-gray-600">
            从小红书视频中提取内容并整合到知识库
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="mb-6">
            <label htmlFor="video-url" className="block text-gray-700 font-medium mb-2">
              小红书视频链接
            </label>
            <div className="relative">
              <input
                type="text"
                id="video-url"
                value={videoUrl}
                onChange={handleInputChange}
                placeholder="请输入小红书视频链接或 xhslink"
                className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition-all ${isValid ? 'border-gray-300 focus:ring-blue-500' : 'border-red-500 focus:ring-red-500'}`}
              />
              {isValid && videoUrl && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-500">
                  ✓
                </div>
              )}
            </div>
          </div>
          
          <button
            type="submit"
            disabled={isProcessing}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-6 rounded-lg transition-all disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isProcessing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>处理中...</span>
              </>
            ) : (
              '开始处理'
            )}
          </button>
        </form>

        {status && (
          <div className={`mb-6 p-4 rounded-lg ${status === '处理成功' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'} flex items-center gap-2`}>
            <div className={`w-6 h-6 flex items-center justify-center rounded-full ${status === '处理成功' ? 'bg-green-500 text-white' : 'bg-yellow-500 text-white'}`}>
              {status === '处理成功' ? '✓' : '!'}
            </div>
            <p className="font-medium">{status}</p>
          </div>
        )}

        {error && (
          <div className="mb-6 p-4 bg-red-100 text-red-700 rounded-lg flex items-center gap-2">
            <div className="w-6 h-6 flex items-center justify-center rounded-full bg-red-500 text-white">
              !
            </div>
            <div>
              <p className="font-medium">错误信息</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div className="mt-8 bg-gray-50 rounded-xl p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              处理结果
            </h2>
            
            <div className="bg-white p-4 rounded-lg mb-4 shadow-sm">
              <h3 className="font-medium text-gray-700 mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                视频信息
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">标题</p>
                  <p className="font-medium truncate">{result.video_info.title}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">作者</p>
                  <p className="font-medium">{result.video_info.author}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">时长</p>
                  <p className="font-medium">{result.video_info.duration} 秒</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">点赞数</p>
                  <p className="font-medium">{result.video_info.likes}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">评论数</p>
                  <p className="font-medium">{result.video_info.comments}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">分享数</p>
                  <p className="font-medium">{result.video_info.shares}</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow-sm">
              <h3 className="font-medium text-gray-700 mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                下载信息
              </h3>
              <p className="text-sm text-gray-500">下载路径</p>
              <p className="font-medium text-blue-600 break-all">{result.download_path}</p>
            </div>
          </div>
        )}

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>© 2026 LLM Wiki Processor</p>
        </div>
      </div>
    </div>
  )
}

export default App
