import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Loader2, Mail, LockKeyhole, UserRound } from "lucide-react";
import { Logo } from "../components/Logo";
import { useAuth } from "../context/AuthContext";

export default function Cadastro() {
  const { signup, loading } = useAuth();
  const nav = useNavigate();
  const [nome,setNome]=useState(""); const [email,setEmail]=useState(""); const [senha,setSenha]=useState(""); const [confirmar,setConfirmar]=useState(""); const [erro,setErro]=useState("");
  async function submit(e:FormEvent){e.preventDefault();setErro("");if(senha.length<8){setErro("A senha precisa ter pelo menos 8 caracteres.");return;}if(senha!==confirmar){setErro("As senhas não coincidem.");return;}try{await signup({nome:nome.trim(),email:email.trim().toLowerCase(),senha});nav("/login",{replace:true,state:{mensagem:"Conta criada! Entre com seu e-mail e senha."}});}catch(err:any){setErro(err?.message||"Não foi possível criar a conta.");}}
  return <div className="min-h-screen bg-slate-50 p-5"><div className="mx-auto max-w-md pt-8 md:pt-16"><Logo/><div className="card mt-8 p-6 md:p-8"><h1 className="text-2xl font-bold">Criar sua conta</h1><p className="mt-1 text-sm text-slate-500">Não é necessário informar telefone.</p>
    {erro&&<div role="alert" className="mt-5 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">{erro}</div>}
    <form onSubmit={submit} className="mt-6 space-y-4">
      <label className="block"><span className="mb-1.5 block text-sm font-medium">Nome</span><div className="relative"><UserRound size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/><input className="input w-full pl-11" value={nome} onChange={e=>setNome(e.target.value)} autoComplete="name" required minLength={2} placeholder="Seu nome"/></div></label>
      <label className="block"><span className="mb-1.5 block text-sm font-medium">E-mail</span><div className="relative"><Mail size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/><input className="input w-full pl-11" type="email" value={email} onChange={e=>setEmail(e.target.value)} autoComplete="email" required placeholder="seu@email.com"/></div></label>
      <label className="block"><span className="mb-1.5 block text-sm font-medium">Senha</span><div className="relative"><LockKeyhole size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/><input className="input w-full pl-11" type="password" value={senha} onChange={e=>setSenha(e.target.value)} autoComplete="new-password" minLength={8} required placeholder="Mínimo de 8 caracteres"/></div></label>
      <label className="block"><span className="mb-1.5 block text-sm font-medium">Confirmar senha</span><input className="input w-full" type="password" value={confirmar} onChange={e=>setConfirmar(e.target.value)} autoComplete="new-password" required placeholder="Digite a senha novamente"/></label>
      <button className="btn-primary w-full" type="submit" disabled={loading}>{loading?<><Loader2 className="animate-spin" size={18}/> Criando...</>:"Criar conta"}</button>
    </form><p className="mt-6 text-center text-sm text-slate-500">Já possui conta? <Link to="/login" className="font-semibold text-slate-900 hover:underline">Entrar</Link></p>
  </div></div></div>;
}
