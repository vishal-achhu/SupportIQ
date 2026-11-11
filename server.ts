import express from 'express';
import cors from 'cors';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();
const port = Number(process.env.PORT ?? 3000);
const target = process.env.PYTHON_API_URL ?? 'http://localhost:8000';

app.use(cors({origin:['http://localhost:5173'],credentials:true}));
app.get('/health', (_req,res)=>res.json({status:'UP',service:'supportiq-gateway'}));
app.use('/api', createProxyMiddleware({
  target,
  changeOrigin:true,
  pathRewrite:{'^/api':''},
  on:{error:(err,_req,res)=>{ if('writeHead' in res) (res as any).writeHead(502,{'Content-Type':'application/json'}); (res as any).end(JSON.stringify({error:'AI service unavailable',detail:err.message})); }}
}));
app.listen(port,()=>console.log(`SupportIQ gateway listening on ${port}`));
