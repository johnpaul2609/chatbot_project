import { useState, useEffect, useCallback } from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

const API = 'http://127.0.0.1:8000/api/admin';

// ── Types ────────────────────────────────────────────────────────────────────
interface Stats {
  total_conversations: number;
  today_conversations: number;
  unique_users: number;
  unanswered_queries: number;
  admission_queries: number;
  academic_queries: number;
  avg_confidence: number;
}
interface TopIntent   { intent: string; count: number; avg_conf: number }
interface DailyData   { date: string; count: number }
interface HourlyData  { hour: number; count: number }
interface Unanswered  { message: string; time: string; user: string }
interface RecentConv  { user: string; message: string; intent: string; confidence: number; time: string }

// ── Auth helper ───────────────────────────────────────────────────────────────
function authHeader(user: string, pass: string) {
  return 'Basic ' + btoa(`${user}:${pass}`);
}

// ── Login Screen ──────────────────────────────────────────────────────────────
function LoginScreen({ onLogin }: { onLogin: (u: string, p: string) => void }) {
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!user || !pass) { setError('Enter username and password'); return; }
    setLoading(true); setError('');
    try {
      const res = await fetch(`${API}/stats`, {
       method: "GET",
       headers: {
         "Authorization": authHeader(user, pass)
       }
      });
      if (res.ok) { onLogin(user, pass); }
      else { setError('Invalid credentials. Try admin / stlourdes2024'); }
    } catch {
      setError('Cannot connect to backend. Make sure server is running.');
    }
    setLoading(false);
  };

  return (
    <div style={{
      minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: "'Georgia', serif"
    }}>
      {/* Animated background dots */}
      <div style={{ position: 'fixed', inset: 0, overflow: 'hidden', pointerEvents: 'none' }}>
        {[...Array(20)].map((_, i) => (
          <div key={i} style={{
            position: 'absolute',
            width: Math.random() * 4 + 1 + 'px',
            height: Math.random() * 4 + 1 + 'px',
            background: 'rgba(147,197,253,0.3)',
            borderRadius: '50%',
            left: Math.random() * 100 + '%',
            top: Math.random() * 100 + '%',
            animation: `pulse ${2 + Math.random() * 3}s ease-in-out infinite`,
          }} />
        ))}
      </div>

      <div style={{
        background: 'rgba(255,255,255,0.05)', backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255,255,255,0.1)', borderRadius: '24px',
        padding: '48px', width: '380px', position: 'relative'
      }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{
            width: '64px', height: '64px', background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
            borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 16px', fontSize: '28px', boxShadow: '0 8px 32px rgba(59,130,246,0.4)'
          }}>🎓</div>
          <h1 style={{ color: '#fff', fontSize: '22px', margin: '0 0 4px', fontWeight: 700, letterSpacing: '-0.5px' }}>
            St Lourdes Admin
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: '13px', margin: 0 }}>
            Chatbot Analytics Dashboard
          </p>
        </div>

        {/* Form */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ color: 'rgba(255,255,255,0.7)', fontSize: '12px', fontFamily: 'monospace', letterSpacing: '0.1em' }}>
              USERNAME
            </label>
            <input
              value={user} onChange={e => setUser(e.target.value)}
              placeholder="admin"
              style={{
                width: '100%', padding: '12px 16px', marginTop: '6px',
                background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.15)',
                borderRadius: '10px', color: '#fff', fontSize: '15px', outline: 'none',
                boxSizing: 'border-box', transition: 'border-color 0.2s',
              }}
              onFocus={e => e.target.style.borderColor = '#3b82f6'}
              onBlur={e => e.target.style.borderColor = 'rgba(255,255,255,0.15)'}
            />
          </div>
          <div>
            <label style={{ color: 'rgba(255,255,255,0.7)', fontSize: '12px', fontFamily: 'monospace', letterSpacing: '0.1em' }}>
              PASSWORD
            </label>
            <input
              type="password" value={pass} onChange={e => setPass(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleLogin()}
              placeholder="••••••••••••"
              style={{
                width: '100%', padding: '12px 16px', marginTop: '6px',
                background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.15)',
                borderRadius: '10px', color: '#fff', fontSize: '15px', outline: 'none',
                boxSizing: 'border-box',
              }}
              onFocus={e => e.target.style.borderColor = '#3b82f6'}
              onBlur={e => e.target.style.borderColor = 'rgba(255,255,255,0.15)'}
            />
          </div>

          {error && (
            <div style={{ background: 'rgba(239,68,68,0.15)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '8px', padding: '10px 14px', color: '#fca5a5', fontSize: '13px' }}>
              ⚠️ {error}
            </div>
          )}

          <button
            onClick={handleLogin} disabled={loading}
            style={{
              padding: '13px', background: loading ? 'rgba(59,130,246,0.5)' : 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
              border: 'none', borderRadius: '10px', color: '#fff', fontSize: '15px',
              fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer',
              boxShadow: '0 4px 16px rgba(59,130,246,0.4)', transition: 'all 0.2s',
              letterSpacing: '0.02em',
            }}
          >
            {loading ? 'Signing in...' : '→ Sign In'}
          </button>
        </div>

        <p style={{ textAlign: 'center', color: 'rgba(255,255,255,0.3)', fontSize: '12px', marginTop: '24px', fontFamily: 'monospace' }}>
          Default: admin / stlourdes2024
        </p>
      </div>
    </div>
  );
}

// ── Stat Card ─────────────────────────────────────────────────────────────────
function StatCard({ label, value, sub, icon, color, bg }: {
  label: string; value: string | number; sub?: string;
  icon: string; color: string; bg: string;
}) {
  return (
    <div style={{
      background: '#fff', borderRadius: '16px', padding: '24px',
      border: '1px solid #e2e8f0', display: 'flex', alignItems: 'flex-start',
      gap: '16px', boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
      transition: 'transform 0.2s, box-shadow 0.2s',
    }}
      onMouseEnter={e => { (e.currentTarget as HTMLDivElement).style.transform = 'translateY(-2px)'; (e.currentTarget as HTMLDivElement).style.boxShadow = '0 8px 24px rgba(0,0,0,0.1)'; }}
      onMouseLeave={e => { (e.currentTarget as HTMLDivElement).style.transform = ''; (e.currentTarget as HTMLDivElement).style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)'; }}
    >
      <div style={{ width: '52px', height: '52px', background: bg, borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '22px', flexShrink: 0 }}>
        {icon}
      </div>
      <div>
        <div style={{ fontSize: '28px', fontWeight: 800, color: '#0f172a', lineHeight: 1, fontFamily: 'Georgia, serif' }}>{value}</div>
        <div style={{ fontSize: '13px', color: '#64748b', marginTop: '4px', fontWeight: 500 }}>{label}</div>
        {sub && <div style={{ fontSize: '11px', color, marginTop: '2px', fontWeight: 600 }}>{sub}</div>}
      </div>
    </div>
  );
}

// ── Section Card ──────────────────────────────────────────────────────────────
function Card({ title, children, action }: { title: string; children: React.ReactNode; action?: React.ReactNode }) {
  return (
    <div style={{ background: '#fff', borderRadius: '16px', border: '1px solid #e2e8f0', overflow: 'hidden', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
      <div style={{ padding: '20px 24px', borderBottom: '1px solid #f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700, color: '#0f172a', fontFamily: 'Georgia, serif' }}>{title}</h3>
        {action}
      </div>
      <div style={{ padding: '20px 24px' }}>{children}</div>
    </div>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────
export default function AdminDashboard() {
  const [auth, setAuth] = useState<{ user: string; pass: string } | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'conversations' | 'unanswered'>('overview');
  const [loading, setLoading] = useState(false);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  const [stats, setStats]         = useState<Stats | null>(null);
  const [topIntents, setTopIntents] = useState<TopIntent[]>([]);
  const [daily, setDaily]         = useState<DailyData[]>([]);
  const [hourly, setHourly]       = useState<HourlyData[]>([]);
  const [unanswered, setUnanswered] = useState<Unanswered[]>([]);
  const [recent, setRecent]       = useState<RecentConv[]>([]);

  const fetchAll = useCallback(async () => {
    if (!auth) return;
    setLoading(true);
    const h = {
      headers: {
       Authorization: authHeader(auth.user, auth.pass)
     }
    };
    try {
      const [s, ti, d, hr, un, rc] = await Promise.all([
        fetch(`${API}/stats`,                h).then(r => r.json()),
        fetch(`${API}/top-intents?limit=10`, h).then(r => r.json()),
        fetch(`${API}/daily-activity?days=14`,h).then(r => r.json()),
        fetch(`${API}/hourly-activity`,       h).then(r => r.json()),
        fetch(`${API}/unanswered?limit=20`,   h).then(r => r.json()),
        fetch(`${API}/recent-conversations?limit=30`, h).then(r => r.json()),
      ]);
      setStats(s); setTopIntents(ti); setDaily(d);
      setHourly(hr); setUnanswered(un); setRecent(rc);
      setLastRefresh(new Date());
    } catch (e) { console.error(e); }
    setLoading(false);
  }, [auth]);

  useEffect(() => { if (auth) fetchAll(); }, [auth, fetchAll]);

  // Auto-refresh every 60s
  useEffect(() => {
    if (!auth) return;
    const t = setInterval(fetchAll, 60000);
    return () => clearInterval(t);
  }, [auth, fetchAll]);

  if (!auth) return <LoginScreen onLogin={(u, p) => setAuth({ user: u, pass: p })} />;

  const PIE_COLORS = ['#3b82f6', '#10b981'];
  const pieData = stats ? [
    { name: 'Admission', value: stats.admission_queries },
    { name: 'Academic',  value: stats.academic_queries  },
  ] : [];

  // Format hour label
  const fmtHour = (h: number) => h === 0 ? '12am' : h < 12 ? `${h}am` : h === 12 ? '12pm' : `${h - 12}pm`;
  const fmtDate = (d: string) => { const dt = new Date(d); return `${dt.getMonth() + 1}/${dt.getDate()}`; };
  const fmtTime = (t: string) => { if (!t) return ''; const dt = new Date(t); return dt.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }); };
  const fmtIntent = (s: string) => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

  const intentColors: Record<string, string> = {
    download: '#10b981', timetable: '#3b82f6', syllabus: '#8b5cf6',
    fees: '#f59e0b', admission: '#ef4444', notes: '#06b6d4',
  };
  const getIntentColor = (intent: string) => {
    for (const [k, v] of Object.entries(intentColors)) if (intent.includes(k)) return v;
    return '#94a3b8';
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f8fafc', fontFamily: "'Trebuchet MS', sans-serif" }}>
      {/* Top Nav */}
      <header style={{
        background: '#fff', borderBottom: '1px solid #e2e8f0', padding: '0 32px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '64px',
        position: 'sticky', top: 0, zIndex: 50, boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '36px', height: '36px', background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px' }}>🎓</div>
          <div>
            <div style={{ fontSize: '15px', fontWeight: 700, color: '#0f172a', fontFamily: 'Georgia, serif' }}>St Lourdes Admin</div>
            <div style={{ fontSize: '11px', color: '#94a3b8' }}>Chatbot Analytics</div>
          </div>
        </div>

        {/* Tabs */}
        <div style={{ display: 'flex', gap: '4px', background: '#f1f5f9', borderRadius: '10px', padding: '4px' }}>
          {(['overview', 'conversations', 'unanswered'] as const).map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)} style={{
              padding: '7px 18px', borderRadius: '7px', border: 'none', cursor: 'pointer',
              fontSize: '13px', fontWeight: 600, transition: 'all 0.2s',
              background: activeTab === tab ? '#fff' : 'transparent',
              color: activeTab === tab ? '#1e40af' : '#64748b',
              boxShadow: activeTab === tab ? '0 1px 3px rgba(0,0,0,0.1)' : 'none',
            }}>
              {tab === 'overview' ? '📊 Overview' : tab === 'conversations' ? '💬 Conversations' : '⚠️ Unanswered'}
            </button>
          ))}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '12px', color: '#94a3b8' }}>
            Updated {lastRefresh.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
          </span>
          <button onClick={fetchAll} disabled={loading} style={{
            padding: '8px 16px', background: loading ? '#e2e8f0' : '#1e40af',
            color: loading ? '#94a3b8' : '#fff', border: 'none', borderRadius: '8px',
            fontSize: '13px', fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer'
          }}>
            {loading ? '⏳' : '↻ Refresh'}
          </button>
          <button onClick={() => setAuth(null)} style={{
            padding: '8px 14px', background: '#fee2e2', color: '#dc2626',
            border: 'none', borderRadius: '8px', fontSize: '13px', fontWeight: 600, cursor: 'pointer'
          }}>
            Sign Out
          </button>
        </div>
      </header>

      <main style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto' }}>

        {/* ── OVERVIEW TAB ── */}
        {activeTab === 'overview' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

            {/* Stat Cards */}
            {stats && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
                <StatCard label="Total Messages"    value={stats.total_conversations.toLocaleString()} icon="💬" color="#10b981" bg="#ecfdf5" sub="All time" />
                <StatCard label="Today"             value={stats.today_conversations} icon="📅" color="#3b82f6" bg="#eff6ff" sub="Today's queries" />
                <StatCard label="Unique Users"      value={stats.unique_users} icon="👥" color="#8b5cf6" bg="#f5f3ff" sub="Sessions" />
                <StatCard label="Unanswered"        value={stats.unanswered_queries} icon="⚠️" color="#ef4444" bg="#fef2f2" sub="Needs improvement" />
                <StatCard label="Admission Queries" value={stats.admission_queries} icon="🎓" color="#f59e0b" bg="#fffbeb" sub="Admission mode" />
                <StatCard label="Academic Queries"  value={stats.academic_queries} icon="📚" color="#06b6d4" bg="#ecfeff" sub="Academic mode" />
                <StatCard label="Avg Confidence"    value={`${stats.avg_confidence}%`} icon="🎯" color="#10b981" bg="#ecfdf5" sub="ML accuracy" />
                <StatCard label="Bot Status"        value="Online" icon="🟢" color="#10b981" bg="#ecfdf5" sub="Running normally" />
              </div>
            )}

            {/* Charts Row 1 */}
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
              <Card title="📈 Daily Message Activity (Last 14 Days)">
                {daily.length === 0 ? (
                  <div style={{ height: 220, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#94a3b8', fontSize: '14px' }}>
                    No data yet — start using the chatbot to see activity
                  </div>
                ) : (
                  <ResponsiveContainer width="100%" height={220}>
                    <LineChart data={daily}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="date" tickFormatter={fmtDate} tick={{ fontSize: 11, fill: '#94a3b8' }} />
                      <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} />
                      <Tooltip
                        contentStyle={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '10px', fontSize: '13px' }}
                        labelFormatter={fmtDate}
                      />
                      <Line type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={2.5} dot={{ r: 4, fill: '#3b82f6' }} activeDot={{ r: 6 }} name="Messages" />
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </Card>

              <Card title="🥧 Admission vs Academic">
                {(stats?.total_conversations ?? 0) === 0 ? (
                  <div style={{ height: 220, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#94a3b8', fontSize: '14px' }}>No data yet</div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <ResponsiveContainer width="100%" height={180}>
                      <PieChart>
                        <Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={4} dataKey="value">
                          {pieData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i]} />)}
                        </Pie>
                        <Tooltip contentStyle={{ borderRadius: '10px', fontSize: '13px' }} />
                      </PieChart>
                    </ResponsiveContainer>
                    <div style={{ display: 'flex', gap: '20px' }}>
                      {pieData.map((d, i) => (
                        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: '#374151' }}>
                          <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: PIE_COLORS[i] }} />
                          {d.name}: <strong>{d.value}</strong>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </Card>
            </div>

            {/* Charts Row 2 */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
              <Card title="⏰ Peak Usage Hours">
                {hourly.every(h => h.count === 0) ? (
                  <div style={{ height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#94a3b8', fontSize: '14px' }}>No data yet</div>
                ) : (
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={hourly} barSize={10}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                      <XAxis dataKey="hour" tickFormatter={h => h % 3 === 0 ? fmtHour(h) : ''} tick={{ fontSize: 10, fill: '#94a3b8' }} />
                      <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} />
                      <Tooltip
                        contentStyle={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '10px', fontSize: '13px' }}
                        labelFormatter={h => `${fmtHour(Number(h))} – ${fmtHour(Number(h) + 1)}`}
                      />
                      <Bar dataKey="count" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Messages" />
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </Card>

              <Card title="🏆 Top Intents">
                {topIntents.length === 0 ? (
                  <div style={{ height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#94a3b8', fontSize: '14px' }}>No data yet</div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '220px', overflowY: 'auto' }}>
                    {topIntents.slice(0, 8).map((intent, i) => (
                      <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span style={{ fontSize: '11px', color: '#94a3b8', width: '16px', textAlign: 'right', fontWeight: 700 }}>{i + 1}</span>
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '3px' }}>
                            <span style={{ fontSize: '12px', fontWeight: 600, color: '#374151', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                              {fmtIntent(intent.intent)}
                            </span>
                            <span style={{ fontSize: '12px', color: '#64748b', flexShrink: 0, marginLeft: '8px' }}>{intent.count}×</span>
                          </div>
                          <div style={{ height: '5px', background: '#f1f5f9', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{
                              height: '100%', borderRadius: '3px',
                              width: `${(intent.count / (topIntents[0]?.count || 1)) * 100}%`,
                              background: getIntentColor(intent.intent),
                              transition: 'width 0.6s ease',
                            }} />
                          </div>
                        </div>
                        <span style={{
                          fontSize: '10px', padding: '2px 6px', borderRadius: '4px',
                          background: intent.avg_conf > 80 ? '#ecfdf5' : intent.avg_conf > 50 ? '#fffbeb' : '#fef2f2',
                          color: intent.avg_conf > 80 ? '#059669' : intent.avg_conf > 50 ? '#d97706' : '#dc2626',
                          fontWeight: 700, flexShrink: 0,
                        }}>
                          {intent.avg_conf}%
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            </div>
          </div>
        )}

        {/* ── CONVERSATIONS TAB ── */}
        {activeTab === 'conversations' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <Card title={`💬 Recent Conversations (${recent.length})`}
              action={<span style={{ fontSize: '12px', color: '#94a3b8' }}>Live feed · auto-refreshes every 60s</span>}
            >
              {recent.length === 0 ? (
                <div style={{ padding: '48px', textAlign: 'center', color: '#94a3b8' }}>No conversations yet</div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: '#f1f5f9', borderRadius: '10px', overflow: 'hidden' }}>
                  {/* Header */}
                  <div style={{ display: 'grid', gridTemplateColumns: '140px 1fr 200px 80px 80px', gap: '12px', padding: '10px 16px', background: '#f8fafc', fontSize: '11px', fontWeight: 700, color: '#64748b', letterSpacing: '0.05em' }}>
                    <span>TIME</span><span>MESSAGE</span><span>INTENT</span><span>MODE</span><span>CONF.</span>
                  </div>
                  {recent.map((c, i) => {
                    const isAcademic = ['syllabus', 'timetable', 'notes', 'download', 'exam', 'faculty', 'attendance', 'library', 'lab', 'project', 'internship', 'academic'].some(k => c.intent.includes(k));
                    return (
                      <div key={i} style={{
                        display: 'grid', gridTemplateColumns: '140px 1fr 200px 80px 80px',
                        gap: '12px', padding: '10px 16px', background: '#fff', fontSize: '13px',
                        borderBottom: '1px solid #f1f5f9', alignItems: 'center',
                        transition: 'background 0.15s',
                      }}
                        onMouseEnter={e => (e.currentTarget as HTMLDivElement).style.background = '#f8fafc'}
                        onMouseLeave={e => (e.currentTarget as HTMLDivElement).style.background = '#fff'}
                      >
                        <span style={{ color: '#94a3b8', fontSize: '12px', fontFamily: 'monospace' }}>
                          {fmtTime(c.time)}
                        </span>
                        <span style={{ color: '#1e293b', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={c.message}>
                          {c.message}
                        </span>
                        <span style={{
                          fontSize: '11px', padding: '3px 8px', borderRadius: '6px', fontWeight: 600,
                          background: getIntentColor(c.intent) + '18',
                          color: getIntentColor(c.intent),
                          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                        }}>
                          {fmtIntent(c.intent)}
                        </span>
                        <span style={{
                          fontSize: '11px', padding: '2px 8px', borderRadius: '6px', fontWeight: 600, textAlign: 'center',
                          background: isAcademic ? '#ecfeff' : '#eff6ff',
                          color: isAcademic ? '#0891b2' : '#1d4ed8',
                        }}>
                          {isAcademic ? 'Academic' : 'Admission'}
                        </span>
                        <span style={{
                          fontSize: '12px', fontWeight: 700, textAlign: 'center',
                          color: c.confidence > 80 ? '#059669' : c.confidence > 50 ? '#d97706' : '#dc2626',
                        }}>
                          {c.confidence}%
                        </span>
                      </div>
                    );
                  })}
                </div>
              )}
            </Card>
          </div>
        )}

        {/* ── UNANSWERED TAB ── */}
        {activeTab === 'unanswered' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: '12px', padding: '16px 20px', display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
              <span style={{ fontSize: '20px' }}>⚠️</span>
              <div>
                <div style={{ fontWeight: 700, color: '#991b1b', fontSize: '14px' }}>Unanswered Queries</div>
                <div style={{ color: '#b91c1c', fontSize: '13px', marginTop: '2px' }}>
                  These are questions the bot couldn't understand. Use them to improve your chatbot's training data.
                </div>
              </div>
            </div>

            <Card title={`⚠️ Unanswered Queries (${unanswered.length})`}>
              {unanswered.length === 0 ? (
                <div style={{ padding: '48px', textAlign: 'center' }}>
                  <div style={{ fontSize: '48px', marginBottom: '12px' }}>🎉</div>
                  <div style={{ color: '#10b981', fontWeight: 700, fontSize: '16px' }}>All queries answered!</div>
                  <div style={{ color: '#94a3b8', fontSize: '13px', marginTop: '4px' }}>The bot handled everything successfully.</div>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {unanswered.map((q, i) => (
                    <div key={i} style={{
                      background: '#fef9f9', border: '1px solid #fecaca', borderRadius: '10px',
                      padding: '14px 18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    }}>
                      <div>
                        <div style={{ fontSize: '14px', color: '#1e293b', fontWeight: 600 }}>"{q.message}"</div>
                        <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px', fontFamily: 'monospace' }}>
                          User: {q.user?.substring(0, 16)}...  ·  {fmtTime(q.time)}
                        </div>
                      </div>
                      <div style={{ fontSize: '11px', padding: '4px 10px', background: '#fee2e2', color: '#dc2626', borderRadius: '6px', fontWeight: 700, flexShrink: 0 }}>
                        UNKNOWN
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </Card>

            {/* Improvement tips */}
            <Card title="💡 How to Improve">
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                {[
                  { icon: '1️⃣', title: 'Add to intent_patterns', desc: 'Open create_database.py and add the unanswered query as a new pattern for the closest intent.' },
                  { icon: '2️⃣', title: 'Create a new intent', desc: 'If the topic is completely new, add a new intent + patterns + response in the database.' },
                  { icon: '3️⃣', title: 'Retrain the classifier', desc: 'Restart the server — the NLP classifier auto-trains on startup using all patterns in the DB.' },
                  { icon: '4️⃣', title: 'Test the fix', desc: 'Open the chatbot and type the same question. It should now get a proper response.' },
                ].map((tip, i) => (
                  <div key={i} style={{ background: '#f8fafc', borderRadius: '10px', padding: '16px', border: '1px solid #e2e8f0' }}>
                    <div style={{ fontSize: '20px', marginBottom: '8px' }}>{tip.icon}</div>
                    <div style={{ fontWeight: 700, color: '#1e293b', fontSize: '13px', marginBottom: '4px' }}>{tip.title}</div>
                    <div style={{ fontSize: '12px', color: '#64748b', lineHeight: 1.5 }}>{tip.desc}</div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
}