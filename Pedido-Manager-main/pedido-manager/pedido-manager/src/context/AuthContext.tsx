
import {
  createContext,
  useContext,
  useMemo,
  useState,
} from "react";

import { api, Login } from "../lib/api";

type AuthContextValue = {
  token: string | null;
  loading: boolean;
  isAdmin: boolean;
  isVisitor: boolean;
  login: (data: Login) => Promise<void>;
  visitorLogin: () => Promise<void>;
  signup: (data: {
    nome: string;
    email: string;
    senha: string;
  }) => Promise<any>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

function obterPayload(token: string | null) {
  if (!token) return null;

  try {
    const parte = token.split(".")[1];

    if (!parte) return null;

    const base64 = parte.replace(/-/g, "+").replace(/_/g, "/");
    const preenchido =
      base64 + "=".repeat((4 - (base64.length % 4)) % 4);

    return JSON.parse(atob(preenchido));
  } catch {
    return null;
  }
}

function isAdminToken(token: string | null) {
  const payload = obterPayload(token);

  if (!payload) return false;

  return (
    payload.admin === true ||
    payload.admin === "true" ||
    payload.funcao === "dono"
  );
}

function isVisitorToken(token: string | null) {
  const payload = obterPayload(token);
  return payload?.visitante === true;
}

export function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem("pedido_token")
  );

  const [loading, setLoading] = useState(false);

  async function login(data: Login) {
    setLoading(true);

    try {
      const result = await api.login(data);

      if (!result?.access_token) {
        throw new Error("A API não retornou o token de acesso.");
      }

      localStorage.setItem("pedido_token", result.access_token);
      setToken(result.access_token);
    } finally {
      setLoading(false);
    }
  }

  async function visitorLogin() {
    setLoading(true);

    try {
      const result = await api.visitanteLogin();

      if (!result?.access_token) {
        throw new Error(
          "A API não retornou o token de visitante."
        );
      }

      localStorage.setItem("pedido_token", result.access_token);
      setToken(result.access_token);
    } finally {
      setLoading(false);
    }
  }

  async function signup(data: {
    nome: string;
    email: string;
    senha: string;
  }) {
    setLoading(true);

    try {
      return await api.criarConta(data);
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("pedido_token");
    setToken(null);
  }

  const value = useMemo(
    () => ({
      token,
      loading,
      isAdmin: isAdminToken(token),
      isVisitor: isVisitorToken(token),
      login,
      visitorLogin,
      signup,
      logout,
    }),
    [token, loading]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const value = useContext(AuthContext);

  if (!value) {
    throw new Error(
      "useAuth deve ser usado dentro de AuthProvider"
    );
  }

  return value;
}
