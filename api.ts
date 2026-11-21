import type {State} from './types';
export const API=process.env.NEXT_PUBLIC_API_URL||'http://127.0.0.1:8000';
export async function request<T=any>(path:string,init?:RequestInit):Promise<T>{const token=typeof window!=='undefined'?localStorage.getItem('nexagri-customer-token'):null;const isForm=typeof FormData!=='undefined'&&init?.body instanceof FormData;const headers:Record<string,string>={...(isForm?{}:{'Content-Type':'application/json'}),...(init?.headers as Record<string,string>||{})};if(token)headers.Authorization=`Bearer ${token}`;const r=await fetch(`${API}${path}`,{...init,headers,cache:'no-store'});const j=await r.json();if(!r.ok)throw new Error(j.detail||'Request failed');return j}
export const state=()=>request<State>('/api/state');
