import { Link, useLocation } from 'react-router-dom';
import './Header.css';

export default function Header() {
  const { pathname } = useLocation();

  return (
    <header className="header">
      <div className="header__inner">
        <Link to="/" className="header__logo">
          <span className="header__logo-mark">VE</span>
          <span className="header__logo-text">
            Virtual<strong>Employee</strong>
          </span>
        </Link>

        <nav className="header__nav">
          <Link
            to="/"
            className={`header__link ${pathname === '/' ? 'header__link--active' : ''}`}
          >
            Home
          </Link>
          <Link
            to="/generate"
            className={`header__link ${pathname === '/generate' ? 'header__link--active' : ''}`}
          >
            Generator
          </Link>
        </nav>

        <Link to="/generate" className="header__cta">
          New Proposal
        </Link>
      </div>
    </header>
  );
}
