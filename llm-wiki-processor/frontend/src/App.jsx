import React, { useState } from 'react'
import './App.css'

function App() {
  const [videoUrl, setVideoUrl] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [status, setStatus] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [isValid, setIsValid] = useState(true)
  const [currentStep, setCurrentStep] = useState(0)
  const [progress, setProgress] = useState(0)
  const [logs, setLogs] = useState([])
  const [showResult, setShowResult] = useState(false)
  const [showProgress, setShowProgress] = useState(false)

  // 步骤定义
  const steps = [
    { id: 0, name: '解析视频链接', icon: '🔍' },
    { id: 1, name: '获取视频信息', icon: '📋' },
    { id: 2, name: '下载视频文件', icon: '📥' },
    { id: 3, name: '提取字幕信息', icon: '📝' },
    { id: 4, name: '保存结果文件', icon: '💾' }
  ]

  // 添加日志
  const addLog = (message, type = 'info') => {
    setLogs(prev => [...prev, { message, type, time: new Date().toLocaleTimeString() }])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // 重置状态
    setIsProcessing(true)
    setShowProgress(true)
    setStatus('正在处理视频...')
    setError('')
    setIsValid(true)
    setResult(null)
    setCurrentStep(0)
    setProgress(0)
    setLogs([])
    setShowResult(false)

    // 表单验证
    if (!videoUrl) {
      setError('请输入小红书视频链接')
      setIsValid(false)
      setIsProcessing(false)
      return
    }

    if (!videoUrl.includes('xiaohongshu.com') && !videoUrl.includes('xhslink.com')) {
      setError('请输入有效的小红书视频链接')
      setIsValid(false)
      setIsProcessing(false)
      return
    }

    addLog('开始处理视频...')

    try {
      // 步骤1: 解析链接
      setCurrentStep(1)
      setProgress(20)
      addLog('正在解析视频链接...')

      const response = await fetch('http://localhost:3001/api/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_url: videoUrl })
      })

      const data = await response.json()
      
      if (data.status === 'success') {
        // 更新进度
        setCurrentStep(4)
        setProgress(100)
        setStatus('处理成功')
        setResult(data)
        setShowResult(true)
        addLog('处理完成！')
      } else {
        throw new Error(data.error || '处理失败')
      }
    } catch (err) {
      setStatus('处理失败')
      setError(err.message)
      addLog(`错误: ${err.message}`, 'error')
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

  // 复制内容
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      addLog('内容已复制到剪贴板')
    }).catch(err => {
      addLog('复制失败: ' + err.message, 'error')
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg p-6 md:p-8">
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

        {/* 处理过程展示 - 始终在处理中和处理完成后都显示 */}
        {showProgress && (
          <div className="mb-8">
            {/* 步骤指示器 */}
            <div className="mb-6">
              <h3 className="font-medium text-gray-700 mb-3">处理进度</h3>
              <div className="flex items-center justify-between relative">
                {steps.map((step, index) => (
                  <div key={step.id} className="flex flex-col items-center z-10">
                    <div 
                      className={`w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold transition-all duration-300 ${
                        index < currentStep || (!isProcessing && showProgress) ? 'bg-green-500 text-white' :
                        index === currentStep ? 'bg-blue-500 text-white animate-pulse' :
                        'bg-gray-200 text-gray-500'
                      }`}
                    >
                      {(index < currentStep || (!isProcessing && showProgress)) ? '✓' : step.icon}
                    </div>
                    <p 
                      className={`mt-2 text-sm ${
                        (index <= currentStep || (!isProcessing && showProgress)) ? 'text-gray-700' : 'text-gray-400'
                      }`}
                    >
                      {step.name}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* 进度条 */}
            <div className="mb-4">
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div 
                  className={`h-2.5 rounded-full transition-all duration-300 ${
                    !isProcessing && progress === 100 ? 'bg-green-500' : 'bg-blue-500'
                  }`}
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-500 mt-1 text-center">{progress}%</p>
            </div>

            {/* 日志展示 */}
            <div className="bg-gray-50 rounded-lg p-4 max-h-48 overflow-y-auto">
              <h4 className="font-medium text-gray-700 mb-2 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2m-5 0h4m-2 0v10" />
                </svg>
                处理日志
              </h4>
              <div className="space-y-1">
                {logs.map((log, index) => (
                  <div 
                    key={index} 
                    className={`text-sm ${log.type === 'error' ? 'text-red-600' : 'text-gray-600'}`}
                  >
                    <span className="text-gray-400 mr-2">[{log.time}]</span>
                    {log.message}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {status && !isProcessing && (
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

        {/* 结果展示 */}
        {result && showResult && (
          <div className="mt-8 bg-gray-50 rounded-xl p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              处理结果
            </h2>
            
            {/* 视频信息 */}
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
                  <p className="font-medium truncate">{result.video_info?.title || '未获取到标题'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">作者</p>
                  <p className="font-medium">{result.video_info?.author || '未知作者'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">视频ID</p>
                  <p className="font-medium">{result.video_info?.video_id || '未知ID'}</p>
                </div>
                {result.video_info?.original_link && (
                  <div>
                    <p className="text-sm text-gray-500">原始链接</p>
                    <p className="font-medium text-blue-600 break-all text-sm">{result.video_info.original_link}</p>
                  </div>
                )}
              </div>
            </div>

            {/* 字幕结果 */}
            {result.subtitle_result && (
              <div className="bg-white p-4 rounded-lg mb-4 shadow-sm">
                <h3 className="font-medium text-gray-700 mb-3 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  字幕信息
                </h3>
                {result.subtitle_result.success ? (
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-500">字幕来源</p>
                      <p className="font-medium">
                        {result.subtitle_result.source === 'metadata' && '视频元数据'}
                        {result.subtitle_result.source === 'video' && '视频内置字幕'}
                        {result.subtitle_result.source === 'audio' && '音频识别（Whisper）'}
                        {!['metadata', 'video', 'audio'].includes(result.subtitle_result.source) && (result.subtitle_result.source || '未知来源')}
                      </p>
                    </div>
                    {result.subtitle_result.confidence && (
                      <div>
                        <p className="text-sm text-gray-500">置信度</p>
                        <p className="font-medium">{Math.round(result.subtitle_result.confidence * 100)}%</p>
                      </div>
                    )}
                    {result.subtitle_result.md_path && (
                      <div>
                        <p className="text-sm text-gray-500">带时间戳文件</p>
                        <p className="font-medium text-blue-600 break-all text-sm">{result.subtitle_result.md_path}</p>
                      </div>
                    )}
                    {result.subtitle_result.text_only_path && (
                      <div>
                        <p className="text-sm text-gray-500">纯文字文件</p>
                        <p className="font-medium text-blue-600 break-all text-sm">{result.subtitle_result.text_only_path}</p>
                      </div>
                    )}
                    
                    {/* 字幕内容预览 */}
                    {result.subtitle_result.subtitles && (
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <p className="text-sm text-gray-500">字幕内容</p>
                          <button
                            onClick={() => copyToClipboard(result.subtitle_result.subtitles)}
                            className="text-xs text-blue-500 hover:text-blue-700"
                          >
                            复制全部
                          </button>
                        </div>
                        <div className="bg-gray-50 p-3 rounded-lg max-h-60 overflow-y-auto text-sm">
                          <pre className="whitespace-pre-wrap">{result.subtitle_result.subtitles}</pre>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="text-red-600">
                    <p className="font-medium">字幕提取失败</p>
                    <p className="text-sm">{result.subtitle_result.error || '未知错误'}</p>
                  </div>
                )}
              </div>
            )}

            {/* 下载信息 */}
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
