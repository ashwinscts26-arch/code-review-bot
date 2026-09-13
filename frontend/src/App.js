import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Code2, Upload, AlertCircle, CheckCircle, FileText, BarChart3,
  Settings, Home, RefreshCw, Share2, Download, Trash2, Eye,
  Menu, X, TrendingUp, TrendingDown, Play, ArrowLeft, Copy,
  ExternalLink, Lock, Globe, Clock
} from 'lucide-react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Design tokens
const COLORS = {
  primary: '#0f172a',
  surface: '#1e293b',
  surfaceLight: '#334155',
  accent: '#3b82f6',
  accentGlow: '#60a5fa',
  danger: '#ef4444',
  warning: '#f97316',
  success: '#10b981',
  text: '#ffffff',
  textSecondary: '#94a3b8',
  border: '#475569',
  critical: '#dc2626',
  high: '#f59e0b',
  medium: '#eab308',
  low: '#22c55e',
};

// Main App Component
export default function CodeReviewBot() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [reviews, setReviews] = useState([]);
  const [selectedReview, setSelectedReview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    loadReviews();
    loadAnalytics();
  }, []);

  const loadReviews = async () => {
    try {
      const response = await axios.get(`${API_URL}/reviews?limit=100`);
      setReviews(response.data.reviews);
    } catch (error) {
      console.error('Failed to load reviews:', error);
    }
  };

  const loadAnalytics = async () => {
    try {
      const response = await axios.get(`${API_URL}/analytics`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    }
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
    setMobileMenuOpen(false);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <DashboardPage onNavigate={handlePageChange} onReviewCreated={loadReviews} />;
      case 'new-review':
        return <NewReviewPage onReviewCreated={() => { loadReviews(); loadAnalytics(); handlePageChange('dashboard'); }} />;
      case 'reviews':
        return <ReviewsPage reviews={reviews} onSelectReview={(review) => { setSelectedReview(review); handlePageChange('review-detail'); }} />;
      case 'review-detail':
        return selectedReview ? <ReviewDetailPage review={selectedReview} onBack={() => handlePageChange('reviews')} /> : null;
      case 'analytics':
        return <AnalyticsPage analytics={analytics} />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <DashboardPage onNavigate={handlePageChange} onReviewCreated={loadReviews} />;
    }
  };

  return (
    <div style={{ backgroundColor: COLORS.primary, color: COLORS.text, minHeight: '100vh' }}>
      {/* Header */}
      <Header currentPage={currentPage} onPageChange={handlePageChange} mobileMenuOpen={mobileMenuOpen} setMobileMenuOpen={setMobileMenuOpen} />

      {/* Mobile Menu */}
      {mobileMenuOpen && <MobileMenu onPageChange={handlePageChange} currentPage={currentPage} />}

      {/* Main Content */}
      <main style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
        {renderPage()}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

// Header Component
function Header({ currentPage, onPageChange, mobileMenuOpen, setMobileMenuOpen }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'new-review', label: 'New Review', icon: Upload },
    { id: 'reviews', label: 'Reviews', icon: FileText },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <header style={{ backgroundColor: COLORS.surface, borderBottom: `1px solid ${COLORS.border}`, position: 'sticky', top: 0, zIndex: 100 }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '16px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }} onClick={() => onPageChange('dashboard')}>
          <Code2 size={32} style={{ color: COLORS.accent }} />
          <div>
            <div style={{ fontSize: '20px', fontWeight: 'bold' }}>Code Review Bot</div>
            <div style={{ fontSize: '12px', color: COLORS.textSecondary }}>AI-Powered Code Analysis</div>
          </div>
        </div>

        {/* Desktop Navigation */}
        <nav style={{ display: 'none', '@media (min-width: 768px)': { display: 'flex' }, gap: '8px' }} className="hidden md:flex">
          {navItems.map((item) => (
            <NavButton key={item.id} item={item} isActive={currentPage === item.id} onClick={() => onPageChange(item.id)} />
          ))}
        </nav>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          style={{ background: 'none', border: 'none', color: COLORS.text, cursor: 'pointer', display: 'flex' }}
          className="md:hidden"
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>
    </header>
  );
}

function NavButton({ item, isActive, onClick }) {
  const Icon = item.icon;
  return (
    <button
      onClick={onClick}
      style={{
        padding: '8px 16px',
        borderRadius: '6px',
        border: 'none',
        backgroundColor: isActive ? COLORS.accent : 'transparent',
        color: isActive ? COLORS.primary : COLORS.text,
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontSize: '14px',
        fontWeight: '500',
        transition: 'all 0.2s',
      }}
    >
      <Icon size={18} />
      <span className="hidden sm:inline">{item.label}</span>
    </button>
  );
}

function MobileMenu({ onPageChange, currentPage }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'new-review', label: 'New Review', icon: Upload },
    { id: 'reviews', label: 'Reviews', icon: FileText },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div style={{ backgroundColor: COLORS.surface, borderBottom: `1px solid ${COLORS.border}` }}>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              style={{
                padding: '12px 20px',
                border: 'none',
                backgroundColor: currentPage === item.id ? COLORS.accent : 'transparent',
                color: currentPage === item.id ? COLORS.primary : COLORS.text,
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '14px',
                fontWeight: '500',
                borderBottom: `1px solid ${COLORS.border}`,
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
              }}
            >
              <Icon size={20} />
              {item.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}

// Dashboard Page
function DashboardPage({ onNavigate, onReviewCreated }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/analytics`);
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>
      {/* Hero */}
      <div style={{ textAlign: 'center', paddingTop: '40px' }}>
        <h1 style={{ fontSize: '48px', fontWeight: 'bold', marginBottom: '16px' }}>Code Review Bot</h1>
        <p style={{ fontSize: '18px', color: COLORS.textSecondary, marginBottom: '32px' }}>
          Find bugs. Catch vulnerabilities. Ship better code.
        </p>
        <button
          onClick={() => onNavigate('new-review')}
          style={{
            padding: '14px 32px',
            backgroundColor: COLORS.accent,
            color: COLORS.primary,
            border: 'none',
            borderRadius: '8px',
            fontSize: '16px',
            fontWeight: '600',
            cursor: 'pointer',
            marginRight: '12px',
            transition: 'all 0.2s',
          }}
        >
          Start Code Review
        </button>
        <button
          onClick={() => onNavigate('reviews')}
          style={{
            padding: '14px 32px',
            backgroundColor: 'transparent',
            color: COLORS.accent,
            border: `2px solid ${COLORS.accent}`,
            borderRadius: '8px',
            fontSize: '16px',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
        >
          View History
        </button>
      </div>

      {/* Stats */}
      {stats && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
          <StatCard label="Reviews Completed" value={stats.total_reviews} icon={<FileText size={32} />} />
          <StatCard label="Average Quality Score" value={`${stats.average_quality_score}/100`} icon={<TrendingUp size={32} />} />
          <StatCard label="Bugs Detected" value={stats.total_bugs} icon={<AlertCircle size={32} />} />
          <StatCard label="Security Issues" value={stats.total_security_issues} icon={<Lock size={32} />} />
        </div>
      )}

      {/* Quick Actions */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
        <ActionCard
          icon={<Upload size={48} />}
          title="Upload Code"
          description="Analyze code by uploading a file"
          onClick={() => onNavigate('new-review')}
        />
        <ActionCard
          icon={<Globe size={48} />}
          title="Paste Code"
          description="Analyze code by pasting directly"
          onClick={() => onNavigate('new-review')}
        />
        <ActionCard
          icon={<BarChart3 size={48} />}
          title="View Analytics"
          description="See trends and statistics"
          onClick={() => onNavigate('analytics')}
        />
      </div>
    </div>
  );
}

function StatCard({ label, value, icon }) {
  return (
    <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ color: COLORS.accent }}>{icon}</div>
      <p style={{ color: COLORS.textSecondary, fontSize: '14px' }}>{label}</p>
      <p style={{ fontSize: '32px', fontWeight: 'bold', color: COLORS.text }}>{value}</p>
    </div>
  );
}

function ActionCard({ icon, title, description, onClick }) {
  return (
    <div
      onClick={onClick}
      style={{
        backgroundColor: COLORS.surface,
        border: `1px solid ${COLORS.border}`,
        borderRadius: '8px',
        padding: '32px',
        textAlign: 'center',
        cursor: 'pointer',
        transition: 'all 0.3s',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = COLORS.accent;
        e.currentTarget.style.transform = 'translateY(-4px)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = COLORS.border;
        e.currentTarget.style.transform = 'translateY(0)';
      }}
    >
      <div style={{ color: COLORS.accent, marginBottom: '16px', display: 'flex', justifyContent: 'center' }}>{icon}</div>
      <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>{title}</h3>
      <p style={{ color: COLORS.textSecondary, fontSize: '14px' }}>{description}</p>
    </div>
  );
}

// New Review Page
function NewReviewPage({ onReviewCreated }) {
  const [code, setCode] = useState('');
  const [filename, setFilename] = useState('');
  const [language, setLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const supportedLanguages = ['python', 'javascript', 'typescript', 'java', 'cpp', 'go', 'ruby', 'csharp', 'php'];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') setDragActive(true);
    else if (e.type === 'dragleave') setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      setFilename(file.name);
      const reader = new FileReader();
      reader.onload = (event) => {
        setCode(event.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files && files[0]) {
      const file = files[0];
      setFilename(file.name);
      const reader = new FileReader();
      reader.onload = (event) => {
        setCode(event.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError('Please enter or upload code');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/analyze`, {
        code,
        filename: filename || 'code.txt',
        language,
      });

      onReviewCreated();
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '32px' }}>New Code Review</h1>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px', marginBottom: '32px' }}>
        {/* Upload Area */}
        <div>
          <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Upload Code File</h3>
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            style={{
              border: `2px dashed ${dragActive ? COLORS.accent : COLORS.border}`,
              borderRadius: '8px',
              padding: '48px',
              textAlign: 'center',
              backgroundColor: dragActive ? COLORS.surfaceLight : COLORS.surface,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            <Upload size={32} style={{ margin: '0 auto 16px', color: COLORS.accent }} />
            <p style={{ color: COLORS.text, fontWeight: '500' }}>Drag & drop your code file here</p>
            <p style={{ color: COLORS.textSecondary, fontSize: '12px', marginTop: '8px' }}>or</p>
            <input
              type="file"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
              id="file-input"
            />
            <label htmlFor="file-input" style={{ color: COLORS.accent, cursor: 'pointer', textDecoration: 'underline', fontSize: '14px' }}>
              click to browse
            </label>
          </div>
          {filename && (
            <p style={{ marginTop: '12px', color: COLORS.success, fontSize: '14px' }}>
              ✓ {filename}
            </p>
          )}
        </div>

        {/* Or Paste */}
        <div>
          <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Or Paste Code</h3>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here..."
            style={{
              width: '100%',
              height: '180px',
              padding: '16px',
              borderRadius: '8px',
              border: `1px solid ${COLORS.border}`,
              backgroundColor: COLORS.surface,
              color: COLORS.text,
              fontFamily: 'monospace',
              fontSize: '13px',
              resize: 'none',
              boxSizing: 'border-box',
            }}
          />
        </div>
      </div>

      {/* Settings */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '32px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>Language</label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            style={{
              width: '100%',
              padding: '10px',
              borderRadius: '6px',
              border: `1px solid ${COLORS.border}`,
              backgroundColor: COLORS.surface,
              color: COLORS.text,
              fontSize: '14px',
              cursor: 'pointer',
              boxSizing: 'border-box',
            }}
          >
            {supportedLanguages.map((lang) => (
              <option key={lang} value={lang} style={{ backgroundColor: COLORS.primary, color: COLORS.text }}>
                {lang.toUpperCase()}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>Filename (optional)</label>
          <input
            type="text"
            value={filename}
            onChange={(e) => setFilename(e.target.value)}
            placeholder="e.g., app.py"
            style={{
              width: '100%',
              padding: '10px',
              borderRadius: '6px',
              border: `1px solid ${COLORS.border}`,
              backgroundColor: COLORS.surface,
              color: COLORS.text,
              fontSize: '14px',
              boxSizing: 'border-box',
            }}
          />
        </div>
      </div>

      {error && (
        <div style={{ backgroundColor: COLORS.danger, color: COLORS.text, padding: '12px', borderRadius: '6px', marginBottom: '20px', fontSize: '14px' }}>
          {error}
        </div>
      )}

      {/* Actions */}
      <div style={{ display: 'flex', gap: '12px' }}>
        <button
          onClick={handleAnalyze}
          disabled={loading || !code}
          style={{
            padding: '12px 32px',
            backgroundColor: loading ? COLORS.surfaceLight : COLORS.accent,
            color: COLORS.primary,
            border: 'none',
            borderRadius: '6px',
            fontSize: '16px',
            fontWeight: '600',
            cursor: loading ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            opacity: loading ? 0.7 : 1,
          }}
        >
          {loading ? <RefreshCw size={18} style={{ animation: 'spin 1s linear infinite' }} /> : <Play size={18} />}
          {loading ? 'Analyzing...' : 'Analyze Code'}
        </button>

        <button
          onClick={() => { setCode(''); setFilename(''); setError(''); }}
          style={{
            padding: '12px 32px',
            backgroundColor: 'transparent',
            color: COLORS.accent,
            border: `1px solid ${COLORS.border}`,
            borderRadius: '6px',
            fontSize: '16px',
            fontWeight: '600',
            cursor: 'pointer',
          }}
        >
          Clear
        </button>
      </div>
    </div>
  );
}

// Reviews Page
function ReviewsPage({ reviews, onSelectReview }) {
  const [filteredReviews, setFilteredReviews] = useState(reviews);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const filtered = reviews.filter((review) =>
      review.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
      review.language.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredReviews(filtered);
  }, [searchTerm, reviews]);

  if (reviews.length === 0) {
    return (
      <div style={{ textAlign: 'center', paddingTop: '60px' }}>
        <FileText size={64} style={{ color: COLORS.textSecondary, margin: '0 auto 20px' }} />
        <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '8px' }}>No reviews yet</h2>
        <p style={{ color: COLORS.textSecondary, marginBottom: '20px' }}>Upload your first code file to get started</p>
      </div>
    );
  }

  return (
    <div>
      <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '32px' }}>Review History</h1>

      <input
        type="text"
        placeholder="Search reviews..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{
          width: '100%',
          maxWidth: '300px',
          padding: '10px 16px',
          borderRadius: '6px',
          border: `1px solid ${COLORS.border}`,
          backgroundColor: COLORS.surface,
          color: COLORS.text,
          fontSize: '14px',
          marginBottom: '20px',
          boxSizing: 'border-box',
        }}
      />

      <div style={{ display: 'grid', gap: '12px' }}>
        {filteredReviews.map((review) => (
          <ReviewCard key={review.id} review={review} onClick={() => onSelectReview(review)} />
        ))}
      </div>
    </div>
  );
}

function ReviewCard({ review, onClick }) {
  const getScoreColor = (score) => {
    if (score >= 80) return COLORS.success;
    if (score >= 60) return COLORS.warning;
    return COLORS.danger;
  };

  return (
    <div
      onClick={onClick}
      style={{
        backgroundColor: COLORS.surface,
        border: `1px solid ${COLORS.border}`,
        borderRadius: '8px',
        padding: '16px',
        display: 'grid',
        gridTemplateColumns: '1fr auto',
        gap: '20px',
        alignItems: 'center',
        cursor: 'pointer',
        transition: 'all 0.2s',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = COLORS.accent;
        e.currentTarget.style.transform = 'translateX(4px)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = COLORS.border;
        e.currentTarget.style.transform = 'translateX(0)';
      }}
    >
      <div>
        <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '8px' }}>{review.filename}</h3>
        <p style={{ color: COLORS.textSecondary, fontSize: '13px', marginBottom: '8px' }}>
          {review.language.toUpperCase()} • {new Date(review.created_at).toLocaleDateString()}
        </p>
        <div style={{ display: 'flex', gap: '20px', fontSize: '13px' }}>
          <span style={{ color: COLORS.textSecondary }}>🐛 {review.bug_count} bugs</span>
          <span style={{ color: COLORS.textSecondary }}>🔒 {review.security_count} security</span>
        </div>
      </div>
      <div style={{ textAlign: 'right' }}>
        <div style={{ fontSize: '28px', fontWeight: 'bold', color: getScoreColor(review.quality_score) }}>
          {review.quality_score}/100
        </div>
        <Eye size={20} style={{ color: COLORS.textSecondary, marginTop: '8px' }} />
      </div>
    </div>
  );
}

// Review Detail Page
function ReviewDetailPage({ review, onBack }) {
  const [shareUrl, setShareUrl] = useState('');
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    try {
      const response = await axios.post(`${API_URL}/share/${review.id}`);
      setShareUrl(response.data.share_url);
    } catch (error) {
      console.error('Failed to create share link:', error);
    }
  };

  const handleCopyShare = () => {
    navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return COLORS.success;
    if (score >= 60) return COLORS.warning;
    return COLORS.danger;
  };

  const getSeverityColor = (severity) => {
    const colorMap = { critical: COLORS.critical, high: COLORS.high, medium: COLORS.medium, low: COLORS.low };
    return colorMap[severity] || COLORS.textSecondary;
  };

  return (
    <div>
      {/* Header */}
      <button
        onClick={onBack}
        style={{
          padding: '8px 16px',
          backgroundColor: 'transparent',
          color: COLORS.accent,
          border: 'none',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: '20px',
          fontSize: '14px',
          fontWeight: '500',
        }}
      >
        <ArrowLeft size={18} /> Back to Reviews
      </button>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>{review.filename}</h1>
          <p style={{ color: COLORS.textSecondary, fontSize: '14px' }}>
            {review.language.toUpperCase()} • {new Date(review.created_at).toLocaleDateString()}
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: getScoreColor(review.quality_score), marginBottom: '8px' }}>
            {review.quality_score}
          </div>
          <p style={{ color: COLORS.textSecondary, fontSize: '12px' }}>Quality Score</p>
        </div>
      </div>

      {/* Score Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '16px', marginBottom: '30px' }}>
        <ScoreBox label="Security" score={review.security_score} />
        <ScoreBox label="Reliability" score={review.reliability_score} />
        <ScoreBox label="Maintainability" score={review.maintainability_score} />
        <ScoreBox label="Complexity" score={review.complexity_score} />
      </div>

      {/* Issues Summary */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '16px', marginBottom: '30px' }}>
        <IssueCountCard label="Critical" count={review.issues.filter((i) => i.severity === 'critical').length} color={COLORS.critical} />
        <IssueCountCard label="High" count={review.issues.filter((i) => i.severity === 'high').length} color={COLORS.high} />
        <IssueCountCard label="Medium" count={review.issues.filter((i) => i.severity === 'medium').length} color={COLORS.medium} />
        <IssueCountCard label="Low" count={review.issues.filter((i) => i.severity === 'low').length} color={COLORS.low} />
      </div>

      {/* Issues List */}
      <div style={{ marginBottom: '30px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>Issues Found</h2>
        {review.issues.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: COLORS.textSecondary' }}>
            <CheckCircle size={48} style={{ margin: '0 auto 16px' }} />
            <p>No issues found! Your code looks great.</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '12px' }}>
            {review.issues.map((issue, idx) => (
              <IssueItem key={idx} issue={issue} getSeverityColor={getSeverityColor} />
            ))}
          </div>
        )}
      </div>

      {/* Code Viewer */}
      {review.code_content && (
        <div style={{ marginBottom: '30px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>Source Code</h2>
          <CodeViewer code={review.code_content} issues={review.issues} />
        </div>
      )}

      {/* Actions */}
      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        <button
          onClick={handleShare}
          style={{
            padding: '10px 16px',
            backgroundColor: COLORS.accent,
            color: COLORS.primary,
            border: 'none',
            borderRadius: '6px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <Share2 size={16} /> Share
        </button>

        <a
          href={`${API_URL}/../export/${review.id}/pdf`}
          style={{
            padding: '10px 16px',
            backgroundColor: COLORS.accent,
            color: COLORS.primary,
            border: 'none',
            borderRadius: '6px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            textDecoration: 'none',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <Download size={16} /> PDF
        </a>
      </div>

      {shareUrl && (
        <div style={{ backgroundColor: COLORS.surfaceLight, padding: '16px', borderRadius: '6px', marginTop: '20px', display: 'flex', gap: '12px', alignItems: 'center' }}>
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Globe size={18} style={{ color: COLORS.accent }} />
            <input
              type="text"
              value={shareUrl}
              readOnly
              style={{
                flex: 1,
                padding: '8px',
                backgroundColor: COLORS.surface,
                border: `1px solid ${COLORS.border}`,
                borderRadius: '4px',
                color: COLORS.text,
                fontSize: '13px',
              }}
            />
          </div>
          <button
            onClick={handleCopyShare}
            style={{
              padding: '8px 16px',
              backgroundColor: COLORS.accent,
              color: COLORS.primary,
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '13px',
              fontWeight: '600',
            }}
          >
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
      )}
    </div>
  );
}

function ScoreBox({ label, score }) {
  const getColor = (score) => {
    if (score >= 80) return COLORS.success;
    if (score >= 60) return COLORS.warning;
    return COLORS.danger;
  };

  return (
    <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '16px', textAlign: 'center' }}>
      <p style={{ color: COLORS.textSecondary, fontSize: '13px', marginBottom: '8px' }}>{label}</p>
      <p style={{ fontSize: '24px', fontWeight: 'bold', color: getColor(score) }}>{score}</p>
    </div>
  );
}

function IssueCountCard({ label, count, color }) {
  return (
    <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '16px', textAlign: 'center' }}>
      <p style={{ fontSize: '24px', fontWeight: 'bold', color }}>{count}</p>
      <p style={{ color: COLORS.textSecondary, fontSize: '13px' }}>{label}</p>
    </div>
  );
}

function IssueItem({ issue, getSeverityColor }) {
  return (
    <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '16px' }}>
      <div style={{ display: 'flex', gap: '12px', alignItems: 'start', marginBottom: '12px' }}>
        <div
          style={{
            padding: '4px 12px',
            backgroundColor: getSeverityColor(issue.severity),
            color: COLORS.primary,
            borderRadius: '4px',
            fontSize: '11px',
            fontWeight: '700',
            whiteSpace: 'nowrap',
            height: 'fit-content',
          }}
        >
          {issue.severity.toUpperCase()}
        </div>
        <div style={{ flex: 1 }}>
          <h4 style={{ fontSize: '14px', fontWeight: '600', marginBottom: '4px' }}>{issue.title}</h4>
          <p style={{ fontSize: '13px', color: COLORS.textSecondary, marginBottom: '8px' }}>Line {issue.line_number}</p>
          <p style={{ fontSize: '13px', color: COLORS.textSecondary }}>{issue.description}</p>
        </div>
      </div>
      {issue.suggested_fix && (
        <div style={{ backgroundColor: COLORS.surfaceLight, padding: '12px', borderRadius: '4px', fontSize: '12px', color: COLORS.textSecondary', marginTop: '8px' }}>
          <strong style={{ color: COLORS.success }}>Suggested fix:</strong> {issue.suggested_fix}
        </div>
      )}
    </div>
  );
}

function CodeViewer({ code, issues }) {
  const lines = code.split('\n');
  const issuesByLine = {};
  issues.forEach((issue) => {
    issuesByLine[issue.line_number] = issue;
  });

  return (
    <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '16px', overflow: 'auto', maxHeight: '600px' }}>
      <pre style={{ margin: 0, fontFamily: 'monospace', fontSize: '13px', color: COLORS.text, lineHeight: '1.6' }}>
        {lines.map((line, idx) => {
          const lineNum = idx + 1;
          const issue = issuesByLine[lineNum];
          const bgColor = issue ? (issue.severity === 'critical' ? '#7f1d1d' : '#664400') : 'transparent';

          return (
            <div key={idx} style={{ backgroundColor: bgColor, display: 'flex', paddingLeft: '12px', borderLeft: issue ? `3px solid ${getSeverityColor(issue.severity)}` : 'none' }}>
              <span style={{ color: COLORS.textSecondary, marginRight: '16px', minWidth: '40px', textAlign: 'right', userSelect: 'none' }}>
                {lineNum}
              </span>
              <span>{line}</span>
            </div>
          );
        })}
      </pre>
    </div>
  );
}

function getSeverityColor(severity) {
  const map = { critical: '#dc2626', high: '#f59e0b', medium: '#eab308', low: '#22c55e' };
  return map[severity] || '#94a3b8';
}

// Analytics Page
function AnalyticsPage({ analytics }) {
  if (!analytics) {
    return <div style={{ textAlign: 'center', padding: '40px' }}>Loading analytics...</div>;
  }

  const languageData = Object.entries(analytics.language_distribution).map(([name, count]) => ({ name, value: count }));
  const severityData = Object.entries(analytics.severity_distribution).map(([name, value]) => ({ name, value }));

  return (
    <div>
      <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '32px' }}>Analytics</h1>

      {/* Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '32px' }}>
        <AnalyticsCard label="Total Reviews" value={analytics.total_reviews} />
        <AnalyticsCard label="Average Quality" value={`${analytics.average_quality_score}/100`} />
        <AnalyticsCard label="Total Bugs" value={analytics.total_bugs} />
        <AnalyticsCard label="Security Issues" value={analytics.total_security_issues} />
      </div>

      {/* Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px' }}>
        {/* Language Distribution */}
        {languageData.length > 0 && (
          <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '20px' }}>
            <h3 style={{ marginBottom: '16px', fontWeight: '600' }}>Languages</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={languageData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80}>
                  {languageData.map((_, idx) => (
                    <Cell key={`cell-${idx}`} fill={[COLORS.accent, COLORS.warning, COLORS.success, COLORS.danger][idx % 4]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}` }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Severity Distribution */}
        {severityData.length > 0 && (
          <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '20px' }}>
            <h3 style={{ marginBottom: '16px', fontWeight: '600' }}>Severity Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={severityData}>
                <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
                <XAxis dataKey="name" stroke={COLORS.textSecondary} />
                <YAxis stroke={COLORS.textSecondary} />
                <Tooltip contentStyle={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}` }} />
                <Bar dataKey="value" fill={COLORS.accent} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Score Trend */}
      {analytics.score_trend && analytics.score_trend.length > 0 && (
        <div style={{ marginTop: '20px', backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginBottom: '16px', fontWeight: '600' }}>Quality Score Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={analytics.score_trend}>
              <defs>
                <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={COLORS.accent} stopOpacity={0.8} />
                  <stop offset="95%" stopColor={COLORS.accent} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
              <XAxis dataKey="date" stroke={COLORS.textSecondary} />
              <YAxis stroke={COLORS.textSecondary} domain={[0, 100]} />
              <Tooltip contentStyle={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}` }} />
              <Area type="monotone" dataKey="score" stroke={COLORS.accent} fillOpacity={1} fill="url(#colorScore)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

function AnalyticsCard({ label, value }) {
  return (
    <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '20px', textAlign: 'center' }}>
      <p style={{ color: COLORS.textSecondary, fontSize: '13px', marginBottom: '8px' }}>{label}</p>
      <p style={{ fontSize: '32px', fontWeight: 'bold', color: COLORS.accent }}>{value}</p>
    </div>
  );
}

// Settings Page
function SettingsPage() {
  return (
    <div style={{ maxWidth: '600px' }}>
      <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '32px' }}>Settings & About</h1>

      <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '24px', marginBottom: '20px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>About Code Review Bot</h2>
        <p style={{ color: COLORS.textSecondary, lineHeight: '1.6', marginBottom: '16px' }}>
          Code Review Bot is an AI-powered code analysis tool that helps developers find bugs, security vulnerabilities, and code quality issues.
        </p>
        <div style={{ color: COLORS.textSecondary, fontSize: '13px' }}>
          <p><strong>Version:</strong> 1.0.0</p>
          <p><strong>Built with:</strong> React, Flask, Claude AI</p>
        </div>
      </div>

      <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '24px', marginBottom: '20px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>Features</h2>
        <ul style={{ color: COLORS.textSecondary, fontSize: '13px', lineHeight: '1.8' }}>
          <li>✓ Static code analysis</li>
          <li>✓ Security vulnerability scanning</li>
          <li>✓ Code quality scoring</li>
          <li>✓ AI-powered insights</li>
          <li>✓ Multiple language support</li>
          <li>✓ PDF and CSV exports</li>
          <li>✓ Shareable review links</li>
          <li>✓ Historical review tracking</li>
        </ul>
      </div>

      <div style={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: '8px', padding: '24px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>Disclaimer</h2>
        <p style={{ color: COLORS.warning, fontSize: '13px', lineHeight: '1.6' }}>
          Code Review Bot is for educational purposes only. While it uses advanced analysis techniques, no automated tool is perfect.
          Always review code with human developers and apply your own judgment before deploying to production.
        </p>
      </div>
    </div>
  );
}

// Footer
function Footer() {
  return (
    <footer style={{ backgroundColor: COLORS.surface, borderTop: `1px solid ${COLORS.border}`, marginTop: '80px', padding: '40px 20px', textAlign: 'center', color: COLORS.textSecondary, fontSize: '13px' }}>
      <p>© 2024 Code Review Bot. Built for better code quality.</p>
    </footer>
  );
}
