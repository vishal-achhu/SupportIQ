const BASE=import.meta.env.VITE_GATEWAY_URL??'http://localhost:3000/api';
export function getToken(){return localStorage.getItem('supportiq_token')}
export async function api<T>(path:string,options:RequestInit={}):Promise<T>{
 const headers=new Headers(options.headers);
 if(!(options.body instanceof FormData)) headers.set('Content-Type','application/json');
 if(getToken())headers.set('Authorization',`Bearer ${getToken()}`);
 const res=await fetch(`${BASE}${path}`,{...options,headers});
 if(!res.ok)throw new Error(await res.text()||`HTTP ${res.status}`);
 return res.json() as Promise<T>;
}
