import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ScatterChart, Scatter
} from 'recharts';
import {
  Code2, Upload, BarChart3, History, Settings, HelpCircle,
  Menu, X, Home, TrendingUp, TrendingDown, AlertCircle,
  CheckCircle, AlertTriangle, ZapOff, Share2, Download,
  Trash2, Eye, ArrowRight, Copy, ExternalLink, Search,
  Filter, ChevronDown, FileText, Search as SearchIcon
} from 'lucide-react';

// ═══════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════

interface Issue {
  id: number;
  type: string;
  severity: string;
  category: string;
  line_number: number;
  title: string;
  description: string;
  explanation?: string;
  impact?: string;
  suggested_fix?: string;
  cwe?: string;
  code_context?: string;
}

interface Review {
  id: number;
  filename: string;
  language: string;
  code_content: string;
  quality_score: number;
  bug_count: number;
  security_count: number;
  suggestion_count: number;
  security_score: number;
  reliability_score: number;
  maintainability_score: number;
  complexity_score: number;
  analysis_duration: number;
  created_at: string;
  issues: Issue[];
}

interface AnalysisResult {
  review_id: number;
  filename: string;
  language: string;
  quality_score: number;
  bug_count: number;
  security_count: number;
  created_at: string;
}

// ═══════════════════════════════════════════════════════════════════
// COLORS & DESIGN TOKENS
// ═══════════════════════════════════════════════════════════════════

const COLORS = {
  bg: '#0f172a',
  surface: '#1e293b',
  surfaceLight: '#334155',
  primary: '#3b82f6',
  primaryLight: '#60a5fa',
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  text: '#f1f5f9',
  textSecondary: '#cbd5e1',
  border: '#334155',
};

const SEVERITY_COLORS = {
  critical: '#dc2626',
  high: '#ea580c',
  medium: '#f59e0b',
  low: '#eab308',
  info: '#06b6d4',
};

// ═══════════════════════════════════════════════════════════════════
// REUSABLE COMPONENTS
// ═══════════════════════════════════════════════════════════════════

const Card: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <div
    className={`rounded-lg border p-6 ${className}`}
    style={{
      backgroundColor: COLORS.surface,
      borderColor: COLORS.border,
    }}
  >
    {children}
  </div>
);

const Button: React.FC<{
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  onClick?: () => void;
  className?: string;
  loading?: boolean;
  disabled?: boolean;
}> = ({ children, variant = 'primary', onClick, className = '', loading = false, disabled = false }) => {
  const variantStyles = {
    primary: { bg: COLORS.primary, text: 'white', hover: COLORS.primaryLight },
    secondary: { bg: 'transparent', text: COLORS.text, hover: COLORS.surfaceLight, border: COLORS.border },
    danger: { bg: COLORS.danger, text: 'white', hover: '#dc2626' },
  };

  const style = variantStyles[variant];

  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`px-4 py-2 rounded-lg font-medium transition-colors ${className}`}
      style={{
        backgroundColor: variant === 'secondary' ? 'transparent' : style.bg,
        color: style.text,
        border: variant === 'secondary' ? `1px solid ${COLORS.border}` : 'none',
        opacity: disabled ? 0.5 : 1,
        cursor: disabled ? 'not-allowed' : 'pointer',
      }}
    >
      {loading ? 'Loading...' : children}
    </button>
  );
};

const Badge: React.FC<{ label: string; value: string | number; color?: string; icon?: React.ReactNode }> = ({
  label,
  value,
  color,
  icon,
}) => (
  <div className="p-4 rounded-lg border" style={{ backgroundColor: COLORS.surfaceLight, borderColor: COLORS.border }}>
    <div className="flex items-center justify-between mb-1">
      <p style={{ color: COLORS.textSecondary }} className="text-sm">
        {label}
      </p>
      {icon && <span style={{ color: color || COLORS.primary }}>{icon}</span>}
    </div>
    <p className="text-2xl font-bold" style={{ color: color || COLORS.text }}>
      {value}
    </p>
  </div>
);

const SeverityBadge: React.FC<{ severity: string }> = ({ severity }) => (
  <span
    className="px-2 py-1 rounded text-xs font-bold"
    style={{
      backgroundColor: SEVERITY_COLORS[severity as keyof typeof SEVERITY_COLORS] + '20',
      color: SEVERITY_COLORS[severity as keyof typeof SEVERITY_COLORS],
    }}
  >
    {severity.toUpperCase()}
  </span>
);

// ═══════════════════════════════════════════════════════════════════
// PAGES
// ═══════════════════════════════════════════════════════════════════

const DashboardPage: React.FC<{ onStartReview: () => void; stats?: any }> = ({ onStartReview, stats }) => (
  <div className="space-y-8">
    {/* Hero */}
    <div className="text-center py-12">
      <h1 className="text-4xl font-bold mb-4" style={{ color: COLORS.text }}>
        Code Review Bot
      </h1>
      <p className="text-lg mb-8" style={{ color: COLORS.textSecondary }}>
        Find bugs. Catch vulnerabilities. Ship better code.
      </p>
      <div className="flex gap-4 justify-center">
        <Button onClick={onStartReview} className="px-8 py-3 text-lg">
          Start Code Review
        </Button>
        <Button variant="secondary" className="px-8 py-3 text-lg">
          View History
        </Button>
      </div>
    </div>

    {/* Stats */}
    {stats && (
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Badge label="Reviews" value={stats.total_reviews || 0} icon={<FileText size={20} />} />
        <Badge label="Avg Score" value={`${Math.round(stats.average_score || 0)}/100`} icon={<BarChart3 size={20} />} color={COLORS.success} />
        <Badge label="Bugs Found" value={stats.total_bugs || 0} icon={<AlertCircle size={20} />} color={COLORS.danger} />
        <Badge label="Security Issues" value={stats.total_security_issues || 0} icon={<AlertTriangle size={20} />} color={COLORS.warning} />
      </div>
    )}

    {/* Quick Actions */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card>
        <Upload size={32} style={{ color: COLORS.primary }} className="mb-4" />
        <h3 className="font-bold text-lg mb-2" style={{ color: COLORS.text }}>
          Upload Code
        </h3>
        <p className="text-sm mb-4" style={{ color: COLORS.textSecondary }}>
          Analyze a file from your computer
        </p>
        <Button variant="secondary" onClick={onStartReview}>
          Upload File
        </Button>
      </Card>

      <Card>
        <Code2 size={32} style={{ color: COLORS.primary }} className="mb-4" />
        <h3 className="font-bold text-lg mb-2" style={{ color: COLORS.text }}>
          Paste Code
        </h3>
        <p className="text-sm mb-4" style={{ color: COLORS.textSecondary }}>
          Paste code directly into the analyzer
        </p>
        <Button variant="secondary" onClick={onStartReview}>
          Paste Code
        </Button>
      </Card>

      <Card>
        <History size={32} style={{ color: COLORS.primary }} className="mb-4" />
        <h3 className="font-bold text-lg mb-2" style={{ color: COLORS.text }}>
          View History
        </h3>
        <p className="text-sm mb-4" style={{ color: COLORS.textSecondary }}>
          Review previous analyses
        </p>
        <Button variant="secondary">View Reviews</Button>
      </Card>
    </div>
  </div>
);

const NewReviewPage: React.FC<{ onReviewComplete: (review: AnalysisResult) => void }> = ({ onReviewComplete }) => {
  const [code, setCode] = useState('');
  const [filename, setFilename] = useState('');
  const [language, setLanguage] = useState('');
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');

  const languages = ['Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Go', 'Ruby', 'PHP'];

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError('Please provide code to analyze');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, filename: filename || 'code.txt', language }),
      });

      if (response.ok) {
        const result = await response.json();
        onReviewComplete(result);
      } else {
        setError('Analysis failed. Please try again.');
      }
    } catch (err) {
      setError('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2" style={{ color: COLORS.text }}>
          New Code Review
        </h1>
        <p style={{ color: COLORS.textSecondary }}>Upload or paste code to analyze</p>
      </div>

      {error && (
        <div className="p-4 rounded-lg" style={{ backgroundColor: COLORS.danger + '20', borderColor: COLORS.danger, borderWidth: 1 }}>
          <p style={{ color: COLORS.danger }}>{error}</p>
        </div>
      )}

      <Card>
        <h2 className="text-lg font-bold mb-4" style={{ color: COLORS.text }}>
          Code Input
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: COLORS.text }}>
              Filename
            </label>
            <input
              type="text"
              placeholder="example.py"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border"
              style={{ backgroundColor: COLORS.bg, borderColor: COLORS.border, color: COLORS.text }}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: COLORS.text }}>
              Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border"
              style={{ backgroundColor: COLORS.bg, borderColor: COLORS.border, color: COLORS.text }}
            >
              <option value="">Auto-detect</option>
              {languages.map((lang) => (
                <option key={lang} value={lang}>
                  {lang}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: COLORS.text }}>
              Code
            </label>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste your code here..."
              rows={15}
              className="w-full px-4 py-2 rounded-lg border font-mono"
              style={{ backgroundColor: COLORS.bg, borderColor: COLORS.border, color: COLORS.text }}
            />
          </div>

          <Button onClick={handleAnalyze} loading={loading} className="w-full py-3 text-lg">
            Analyze Code
          </Button>
        </div>
      </Card>
    </div>
  );
};

const ReviewDetailPage: React.FC<{ reviewId: number; onBack: () => void }> = ({ reviewId, onBack }) => {
  const [review, setReview] = useState<Review | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState('overview');
  const [expandedIssue, setExpandedIssue] = useState<number | null>(null);

  useEffect(() => {
    fetchReview();
  }, [reviewId]);

  const fetchReview = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/review/${reviewId}`);
      if (response.ok) {
        setReview(await response.json());
      }
    } catch (err) {
      console.error('Error fetching review');
    } finally {
      setLoading(false);
    }
  };

  if (loading || !review) return <div>Loading...</div>;

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'bugs', label: `Bugs (${review.bug_count})` },
    { id: 'security', label: `Security (${review.security_count})` },
    { id: 'quality', label: `Quality (${review.suggestion_count})` },
    { id: 'code', label: 'Code' },
  ];

  const filteredIssues =
    selectedTab === 'overview'
      ? review.issues
      : review.issues.filter((i) => i.type === (selectedTab === 'bugs' ? 'bug' : selectedTab === 'security' ? 'security' : 'quality'));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Button variant="secondary" onClick={onBack} className="mb-4">
            ← Back
          </Button>
          <h1 className="text-3xl font-bold" style={{ color: COLORS.text }}>
            {review.filename}
          </h1>
          <p style={{ color: COLORS.textSecondary }}>{review.language} • Analysis: {new Date(review.created_at).toLocaleDateString()}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => window.open(`http://localhost:5000/api/export/${reviewId}/pdf`)}>
            <Download size={18} className="mr-2" />
            PDF
          </Button>
          <Button variant="secondary">
            <Share2 size={18} className="mr-2" />
            Share
          </Button>
        </div>
      </div>

      {/* Scores */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Badge label="Overall" value={review.quality_score} color={review.quality_score >= 70 ? COLORS.success : COLORS.warning} />
        <Badge label="Security" value={review.security_score} />
        <Badge label="Reliability" value={review.reliability_score} />
        <Badge label="Maintainability" value={review.maintainability_score} />
        <Badge label="Complexity" value={review.complexity_score} />
      </div>

      {/* Tabs */}
      <div className="border-b" style={{ borderColor: COLORS.border }}>
        <div className="flex gap-4 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedTab(tab.id)}
              className="px-4 py-3 font-medium border-b-2 transition-colors"
              style={{
                borderColor: selectedTab === tab.id ? COLORS.primary : 'transparent',
                color: selectedTab === tab.id ? COLORS.primary : COLORS.textSecondary,
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {selectedTab === 'code' ? (
        <Card>
          <pre
            className="p-4 rounded overflow-x-auto text-sm"
            style={{ backgroundColor: COLORS.bg, color: COLORS.text }}
          >
            {review.code_content}
          </pre>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredIssues.length === 0 ? (
            <Card>
              <p style={{ color: COLORS.textSecondary }} className="text-center py-8">
                No {selectedTab} issues found
              </p>
            </Card>
          ) : (
            filteredIssues.map((issue) => (
              <Card key={issue.id} className="cursor-pointer" onClick={() => setExpandedIssue(expandedIssue === issue.id ? null : issue.id)}>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <SeverityBadge severity={issue.severity} />
                      <span style={{ color: COLORS.textSecondary }} className="text-sm">
                        Line {issue.line_number}
                      </span>
                    </div>
                    <h3 className="font-bold text-lg mb-2" style={{ color: COLORS.text }}>
                      {issue.title}
                    </h3>
                    <p style={{ color: COLORS.textSecondary }} className="text-sm mb-2">
                      {issue.category}
                    </p>
                    {expandedIssue === issue.id && (
                      <div className="mt-4 space-y-3" style={{ color: COLORS.textSecondary }} className="text-sm">
                        <div>
                          <p className="font-bold" style={{ color: COLORS.text }}>
                            Description
                          </p>
                          <p>{issue.description}</p>
                        </div>
                        {issue.impact && (
                          <div>
                            <p className="font-bold" style={{ color: COLORS.text }}>
                              Impact
                            </p>
                            <p>{issue.impact}</p>
                          </div>
                        )}
                        {issue.suggested_fix && (
                          <div>
                            <p className="font-bold" style={{ color: COLORS.text }}>
                              Suggested Fix
                            </p>
                            <p>{issue.suggested_fix}</p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                  <ChevronDown
                    size={20}
                    style={{ color: COLORS.textSecondary, transform: expandedIssue === issue.id ? 'rotate(180deg)' : 'none' }}
                  />
                </div>
              </Card>
            ))
          )}
        </div>
      )}
    </div>
  );
};

const HistoryPage: React.FC = () => {
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/history');
      if (response.ok) {
        const data = await response.json();
        setReviews(data.reviews || []);
      }
    } catch (err) {
      console.error('Error fetching history');
    } finally {
      setLoading(false);
    }
  };

  const filtered = reviews.filter((r) => r.filename.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-4" style={{ color: COLORS.text }}>
          Review History
        </h1>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Search reviews..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 px-4 py-2 rounded-lg border"
            style={{ backgroundColor: COLORS.surface, borderColor: COLORS.border, color: COLORS.text }}
          />
        </div>
      </div>

      {loading ? (
        <p style={{ color: COLORS.textSecondary }}>Loading...</p>
      ) : filtered.length === 0 ? (
        <Card>
          <p style={{ color: COLORS.textSecondary }} className="text-center py-12">
            No reviews yet. Start by uploading code to analyze.
          </p>
        </Card>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr style={{ borderBottomColor: COLORS.border }} className="border-b">
                <th className="text-left px-4 py-3" style={{ color: COLORS.textSecondary }}>
                  Filename
                </th>
                <th className="text-left px-4 py-3" style={{ color: COLORS.textSecondary }}>
                  Language
                </th>
                <th className="text-right px-4 py-3" style={{ color: COLORS.textSecondary }}>
                  Score
                </th>
                <th className="text-right px-4 py-3" style={{ color: COLORS.textSecondary }}>
                  Bugs
                </th>
                <th className="text-right px-4 py-3" style={{ color: COLORS.textSecondary }}>
                  Security
                </th>
                <th className="text-left px-4 py-3" style={{ color: COLORS.textSecondary }}>
                  Date
                </th>
                <th className="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((review) => (
                <tr key={review.id} style={{ borderBottomColor: COLORS.border }} className="border-b hover:bg-opacity-50">
                  <td className="px-4 py-3" style={{ color: COLORS.text }}>
                    {review.filename}
                  </td>
                  <td className="px-4 py-3" style={{ color: COLORS.textSecondary }}>
                    {review.language}
                  </td>
                  <td className="text-right px-4 py-3">
                    <span
                      style={{
                        color: review.quality_score >= 70 ? COLORS.success : COLORS.warning,
                      }}
                      className="font-bold"
                    >
                      {review.quality_score}
                    </span>
                  </td>
                  <td className="text-right px-4 py-3" style={{ color: COLORS.text }}>
                    {review.bug_count}
                  </td>
                  <td className="text-right px-4 py-3" style={{ color: COLORS.text }}>
                    {review.security_count}
                  </td>
                  <td className="px-4 py-3" style={{ color: COLORS.textSecondary }}>
                    {new Date(review.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3">
                    <Eye size={18} style={{ color: COLORS.primary, cursor: 'pointer' }} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

const AnalyticsPage: React.FC = () => {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/stats');
      if (response.ok) {
        setStats(await response.json());
      }
    } catch (err) {
      console.error('Error fetching stats');
    }
  };

  if (!stats) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold" style={{ color: COLORS.text }}>
        Analytics
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Badge label="Total Reviews" value={stats.total_reviews} icon={<FileText size={20} />} />
        <Badge label="Avg Score" value={Math.round(stats.average_score)} icon={<BarChart3 size={20} />} color={COLORS.success} />
        <Badge label="Total Issues" value={stats.total_issues} icon={<AlertCircle size={20} />} />
        <Badge label="Avg Bugs/Review" value={(stats.total_bugs / stats.total_reviews).toFixed(1)} />
      </div>

      {/* Severity Distribution */}
      <Card>
        <h2 className="text-lg font-bold mb-4" style={{ color: COLORS.text }}>
          Issues by Severity
        </h2>
        {stats.severity_distribution && (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={[
                { name: 'Critical', value: stats.severity_distribution.critical },
                { name: 'High', value: stats.severity_distribution.high },
                { name: 'Medium', value: stats.severity_distribution.medium },
                { name: 'Low', value: stats.severity_distribution.low },
              ]}
            >
              <CartesianGrid stroke={COLORS.border} strokeDasharray="3 3" />
              <XAxis dataKey="name" stroke={COLORS.textSecondary} />
              <YAxis stroke={COLORS.textSecondary} />
              <Tooltip contentStyle={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}` }} />
              <Bar dataKey="value" fill={COLORS.primary} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </Card>

      {/* Language Distribution */}
      {stats.language_distribution && Object.keys(stats.language_distribution).length > 0 && (
        <Card>
          <h2 className="text-lg font-bold mb-4" style={{ color: COLORS.text }}>
            Languages Analyzed
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={Object.entries(stats.language_distribution).map(([name, value]) => ({ name, value }))}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill={COLORS.primary}
                dataKey="value"
              >
                {Object.entries(stats.language_distribution).map((_, idx) => (
                  <Cell key={`cell-${idx}`} fill={[COLORS.primary, COLORS.success, COLORS.warning, COLORS.danger][idx % 4]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: COLORS.surface, border: `1px solid ${COLORS.border}` }} />
            </PieChart>
          </ResponsiveContainer>
        </Card>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════════════════════════

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [selectedReviewId, setSelectedReviewId] = useState<number | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/stats');
      if (response.ok) {
        setStats(await response.json());
      }
    } catch (err) {
      console.error('Error fetching stats');
    }
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'new-review', label: 'New Review', icon: Upload },
    { id: 'history', label: 'History', icon: History },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const renderPage = () => {
    if (currentPage === 'dashboard') {
      return <DashboardPage onStartReview={() => setCurrentPage('new-review')} stats={stats} />;
    } else if (currentPage === 'new-review') {
      return (
        <NewReviewPage
          onReviewComplete={(review) => {
            setSelectedReviewId(review.review_id);
            setCurrentPage('review-detail');
            fetchStats();
          }}
        />
      );
    } else if (currentPage === 'review-detail' && selectedReviewId) {
      return <ReviewDetailPage reviewId={selectedReviewId} onBack={() => setCurrentPage('history')} />;
    } else if (currentPage === 'history') {
      return <HistoryPage />;
    } else if (currentPage === 'analytics') {
      return <AnalyticsPage />;
    }
    return <DashboardPage onStartReview={() => setCurrentPage('new-review')} stats={stats} />;
  };

  return (
    <div style={{ backgroundColor: COLORS.bg, color: COLORS.text, minHeight: '100vh' }}>
      {/* Header */}
      <header
        className="sticky top-0 z-40 border-b"
        style={{ backgroundColor: COLORS.surface, borderColor: COLORS.border }}
      >
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentPage('dashboard')}>
            <Code2 size={32} style={{ color: COLORS.primary }} />
            <div>
              <h1 className="text-xl font-bold">Code Review Bot</h1>
              <p className="text-xs" style={{ color: COLORS.textSecondary }}>
                Upload. Analyze. Improve.
              </p>
            </div>
          </div>

          <button className="md:hidden p-2" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>

          <nav className="hidden md:flex gap-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setCurrentPage(item.id)}
                className="px-3 py-2 rounded-lg flex items-center gap-2 transition-colors text-sm"
                style={{
                  backgroundColor: currentPage === item.id ? COLORS.primary : 'transparent',
                  color: currentPage === item.id ? 'white' : COLORS.text,
                }}
              >
                <item.icon size={18} />
                <span className="hidden lg:inline">{item.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {mobileMenuOpen && (
          <div style={{ backgroundColor: COLORS.surface, borderColor: COLORS.border }} className="border-t">
            <div className="flex flex-col">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    setCurrentPage(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className="px-4 py-3 flex items-center gap-2 border-b text-left"
                  style={{
                    backgroundColor: currentPage === item.id ? COLORS.border : 'transparent',
                    borderColor: COLORS.border,
                    color: COLORS.text,
                  }}
                >
                  <item.icon size={18} />
                  <span>{item.label}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">{renderPage()}</main>

      {/* Footer */}
      <footer
        className="mt-16 border-t py-8"
        style={{ backgroundColor: COLORS.surface, borderColor: COLORS.border }}
      >
        <div className="max-w-7xl mx-auto px-4 text-center" style={{ color: COLORS.textSecondary }}>
          <p className="text-sm">
            © 2024 Code Review Bot. AI-powered static analysis with Claude integration.
          </p>
        </div>
      </footer>
    </div>
  );
}
