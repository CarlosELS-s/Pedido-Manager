
import { FormEvent, useState } from "react";
import {
  ArrowRight,
  LockKeyhole,
  Mail,
  Loader2,
  Eye,
} from "lucide-react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Logo } from "../components/Logo";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login, loading, visitorLogin } = useAuth();
  const nav = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [erro, setErro] = useState("");
  const [entrandoVisitante, setEntrandoVisitante] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setErro("");

    try {
      await login({
        email: email.trim().toLowerCase(),
        senha,
      });

      nav((location.state as any)?.from || "/dashboard", {
        replace: true,
      });
    } catch (error: any) {
      setErro(error?.message || "Não foi possível entrar na sua conta.");
    }
  }

  async function entrarComoVisitante() {
    setErro("");
    setEntrandoVisitante(true);

    try {
      await visitorLogin();

      nav("/dashboard", {
        replace: true,
      });
    } catch (error: any) {
      setErro(
        error?.message || "Não foi possível entrar como visitante."
      );
    } finally {
      setEntrandoVisitante(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="grid min-h-screen lg:grid-cols-2">

        {/* PAINEL ESQUERDO */}
        <div
          className="relative hidden overflow-hidden lg:flex"
          style={{ backgroundColor: "#020617" }}
        >
          <div className="flex w-full flex-col justify-between p-12 xl:p-16">

            <Logo dark />

            <div className="max-w-xl">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-400">
                Gestão simples
              </p>

              <h2 className="mt-5 text-5xl font-bold leading-tight text-white">
                Todos os seus
                <br />
                pedidos em um só
                <br />
                lugar.
              </h2>

              <p className="mt-6 max-w-lg text-lg leading-8 text-slate-400">
                Acompanhe pedidos, itens e status com uma interface rápida e
                objetiva.
              </p>
            </div>

            <p className="text-sm text-slate-500">
              PedidoManager © {new Date().getFullYear()}
            </p>
          </div>
        </div>

        {/* PAINEL DIREITO */}
        <div className="flex items-center justify-center p-5 sm:p-8">
          <div className="w-full max-w-md">

            <div className="mb-8 lg:hidden">
              <Logo />
            </div>

            <div>
              <p className="text-sm font-medium text-slate-500">
                Bem-vindo
              </p>

              <h1 className="mt-1 text-3xl font-bold text-slate-900">
                Entrar
              </h1>

              <p className="mt-2 text-sm text-slate-500">
                Acesse sua conta com e-mail e senha.
              </p>
            </div>

            {(location.state as any)?.mensagem && (
              <div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
                {(location.state as any).mensagem}
              </div>
            )}

            {erro && (
              <div
                role="alert"
                className="mt-5 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700"
              >
                {erro}
              </div>
            )}

            {/* LOGIN NORMAL */}
            <form onSubmit={submit} className="mt-7 space-y-5">

              <label className="block">
                <span className="mb-1.5 block text-sm font-medium text-slate-900">
                  E-mail
                </span>

                <div className="relative">
                  <Mail
                    size={18}
                    className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
                  />

                  <input
                    type="email"
                    autoComplete="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="seu@email.com"
                    className="input w-full pl-11"
                    required
                  />
                </div>
              </label>

              <label className="block">
                <span className="mb-1.5 block text-sm font-medium text-slate-900">
                  Senha
                </span>

                <div className="relative">
                  <LockKeyhole
                    size={18}
                    className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
                  />

                  <input
                    type={mostrarSenha ? "text" : "password"}
                    autoComplete="current-password"
                    value={senha}
                    onChange={(e) => setSenha(e.target.value)}
                    placeholder="Digite sua senha"
                    className="input w-full pl-11 pr-11"
                    required
                  />

                  <button
                    type="button"
                    onClick={() => setMostrarSenha((atual) => !atual)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700"
                    aria-label={mostrarSenha ? "Ocultar senha" : "Mostrar senha"}
                  >
                    {mostrarSenha ? (
                      <span className="text-xs font-semibold">Ocultar</span>
                    ) : (
                      <span className="text-xs font-semibold">Mostrar</span>
                    )}
                  </button>
                </div>
              </label>

              <div className="text-right">
                <Link
                  to="/esqueci-senha"
                  className="text-sm font-semibold text-slate-700 hover:underline"
                >
                  Esqueci minha senha
                </Link>
              </div>

              <button
                type="submit"
                disabled={loading || entrandoVisitante}
                className="btn-primary w-full"
              >
                {loading ? (
                  <>
                    <Loader2 size={18} className="animate-spin" />
                    Entrando...
                  </>
                ) : (
                  <>
                    Entrar
                    <ArrowRight size={18} />
                  </>
                )}
              </button>
            </form>

            {/* DIVISOR */}
            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-slate-200" />
              <span className="text-xs font-medium uppercase text-slate-400">
                Ou
              </span>
              <div className="h-px flex-1 bg-slate-200" />
            </div>

            {/* ENTRAR COMO VISITANTE */}
            <button
              type="button"
              onClick={entrarComoVisitante}
              disabled={loading || entrandoVisitante}
              className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-3 font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {entrandoVisitante ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  Entrando como visitante...
                </>
              ) : (
                <>
                  <Eye size={18} />
                  Entrar como visitante
                </>
              )}
            </button>

            <p className="mt-2 text-center text-xs text-slate-500">
              Acesse uma demonstração com pedidos fictícios.
            </p>

            <p className="mt-7 text-center text-sm text-slate-500">
              Ainda não possui conta?{" "}
              <Link
                to="/cadastro"
                className="font-semibold text-slate-900 hover:underline"
              >
                Criar conta
              </Link>
            </p>

          </div>
        </div>
      </div>
    </div>
  );
}
