
import { Navigate, Outlet, useLocation } from "react-router-dom";

type ProtectedRouteProps = {
  children?: React.ReactNode;
};

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const location = useLocation();
  const token = localStorage.getItem("pedido_token");

  if (!token) {
    return (
      <Navigate
        to="/login"
        replace
        state={{ from: location.pathname }}
      />
    );
  }

  // Visitantes podem navegar pelas páginas protegidas.
  // O backend continuará controlando quais dados podem acessar.
  return children ? <>{children}</> : <Outlet />;
}
