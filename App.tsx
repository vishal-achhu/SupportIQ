import {useState} from 'react';
import type {FormEvent, ChangeEvent} from 'react';
import {Bot,FileText,MessageSquare,Ticket,UploadCloud,LogOut,Send,Plus,ShieldCheck} from 'lucide-react';
import {api,getToken} from './api';

type Source={filename:string;excerpt:string};
type TicketItem={id:number;subject:string;description:string;status:string;priority:string};
export default function App(){
 const [logged,setLogged]=useState(Boolean(getToken()));
 const [email,setEmail]=useState('demo@supportiq.test'),[password,setPassword]=useState('');
 const [name,setName]=useState('Demo User'),[register,setRegister]=useState(false);
 const [question,setQuestion]=useState('What is the refund policy?'),[answer,setAnswer]=useState(''),[sources,setSources]=useState<Source[]>([]);
 const [docs,setDocs]=useState<{id:number;filename:string}[]>([]),[tickets,setTickets]=useState<TicketItem[]>([]);
 const [subject,setSubject]=useState(''),[description,setDescription]=useState('');
 const [notice,setNotice]=useState(''),[busy,setBusy]=useState(false);
 async function auth(e:FormEvent){
  e.preventDefault();setBusy(true);
  try{
   if(register)await api('/auth/register',{method:'POST',body:JSON.stringify({name,email,password})});
   const r=await api<{accessToken:string}>('/auth/login',{method:'POST',body:JSON.stringify({email,password})});
   localStorage.setItem('supportiq_token',r.accessToken);setLogged(true);setNotice('Signed in successfully');
  }catch(err){setNotice(err instanceof Error?err.message:'Authentication failed')}finally{setBusy(false)}
 }
 async function load(){
  try{const [d,t]=await Promise.all([api<typeof docs>('/documents'),api<TicketItem[]>('/tickets')]);setDocs(d);setTickets(t)}
  catch(e){setNotice(e instanceof Error?e.message:'Unable to load workspace')}
 }
 async function upload(e:ChangeEvent<HTMLInputElement>){
  const file=e.target.files?.[0];if(!file)return;
  const form=new FormData();form.append('file',file);setBusy(true);
  try{await api('/documents/upload',{method:'POST',body:form});setNotice('Document processed and indexed');await load()}
  catch(err){setNotice(err instanceof Error?err.message:'Upload failed')}finally{setBusy(false);e.target.value=''}
 }
 async function ask(e:FormEvent){
  e.preventDefault();setBusy(true);setAnswer('');setSources([]);
  try{const r=await api<{answer:string;sources:Source[]}>('/chat/ask',{method:'POST',body:JSON.stringify({question,top_k:5})});setAnswer(r.answer);setSources(r.sources)}
  catch(err){setNotice(err instanceof Error?err.message:'Question failed')}finally{setBusy(false)}
 }
 async function createTicket(e:FormEvent){
  e.preventDefault();try{await api('/tickets',{method:'POST',body:JSON.stringify({subject,description,priority:'NORMAL'})});setSubject('');setDescription('');setNotice('Ticket created');await load()}
  catch(err){setNotice(err instanceof Error?err.message:'Ticket creation failed')}
 }
 if(!logged)return <div className="auth"><form onSubmit={auth} className="auth-card"><div className="logo"><Bot/></div><p className="eyebrow">KNOWLEDGE INTELLIGENCE</p><h1>{register?'Create your workspace':'Welcome to SupportIQ'}</h1><p className="muted">Grounded AI answers for customer support teams.</p>
 {register&&<label>Your name<input value={name} onChange={e=>setName(e.target.value)} required/></label>}
 <label>Work email<input type="email" value={email} onChange={e=>setEmail(e.target.value)} required/></label><label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} minLength={10} required/></label>
 <button className="primary" disabled={busy}>{busy?'Please wait':register?'Create account':'Sign in'}</button><button type="button" className="link" onClick={()=>setRegister(!register)}>{register?'Already registered? Sign in':'New here? Create account'}</button>{notice&&<p className="notice">{notice}</p>}</form></div>;
 return <div className="app"><aside className="sidebar"><div className="brand"><span className="logo"><Bot/></span><b>SupportIQ</b></div><p className="nav-label">WORKSPACE</p><a className="nav active"><MessageSquare/> Knowledge assistant</a><a className="nav"><FileText/> Knowledge base</a><a className="nav"><Ticket/> Support tickets</a><div className="side-foot"><ShieldCheck/> Secure workspace <button onClick={()=>{localStorage.removeItem('supportiq_token');setLogged(false)}}><LogOut size={15}/> Sign out</button></div></aside>
 <main className="main"><header><div><p className="eyebrow">AI SUPPORT WORKSPACE</p><h1>Knowledge assistant</h1><p className="muted">Ask questions grounded in your team's uploaded documents.</p></div><button className="outline" onClick={()=>void load()}>Refresh workspace</button></header>
 {notice&&<div className="notice">{notice}</div>}
 <div className="layout"><section className="panel chat"><div className="panel-title"><div className="round"><Bot/></div><div><b>SupportIQ Assistant</b><small>Document-grounded responses</small></div><span className="online">● READY</span></div>
 <div className="conversation"><div className="bubble bot">Hello! I can answer questions using the documents in your knowledge base. Upload your support material, then ask a question.</div>
 {answer&&<><div className="bubble user">{question}</div><div className="bubble bot">{answer}</div>{sources.length>0&&<div className="sources"><b>Sources used</b>{sources.map((s,i)=><div className="source" key={i}><FileText size={15}/><span><b>{s.filename}</b><small>{s.excerpt}</small></span></div>)}</div>}</>}
 </div><form className="ask" onSubmit={ask}><input value={question} onChange={e=>setQuestion(e.target.value)} placeholder="Ask about refunds, onboarding, policies..." required/><button className="primary" disabled={busy}><Send size={16}/></button></form>
 </section>
 <section className="panel knowledge"><div className="section-head"><div><p className="eyebrow">YOUR KNOWLEDGE</p><h2>Knowledge base</h2></div><span className="counter">{docs.length} files</span></div>
 <label className="upload"><UploadCloud/><b>Upload knowledge document</b><small>PDF, DOCX, TXT or Markdown · 10 MB max</small><input type="file" accept=".pdf,.docx,.txt,.md" onChange={upload}/></label>
 <div className="doc-list">{docs.map(d=><div className="doc" key={d.id}><FileText/><span>{d.filename}</span></div>)}{!docs.length&&<p className="empty">No documents uploaded yet.</p>}</div>
 <div className="section-head ticket-head"><div><p className="eyebrow">CUSTOMER OPERATIONS</p><h2>Support tickets</h2></div><span className="counter">{tickets.length}</span></div>
 <form className="ticket-form" onSubmit={createTicket}><input placeholder="Ticket subject" value={subject} onChange={e=>setSubject(e.target.value)} required/><textarea placeholder="Describe the issue..." value={description} onChange={e=>setDescription(e.target.value)} required/><button className="outline"><Plus size={15}/> Create ticket</button></form>
 <div className="ticket-list">{tickets.slice(0,4).map(t=><div className="ticket" key={t.id}><b>{t.subject}</b><span>{t.status.replace('_',' ')}</span></div>)}{!tickets.length&&<p className="empty">No support tickets yet.</p>}</div>
 </section></div><footer>SupportIQ · FastAPI AI service · Node.js gateway · React + TypeScript</footer></main></div>;
}
