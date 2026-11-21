'use client';
import Link from 'next/link';
import {useLanguage} from './I18nProvider';
import {useCustomer} from './CustomerProvider';
export function Navbar(){const {lang,setLang,t}=useLanguage(),{customer}=useCustomer();return <header className="topbar"><div className="breadcrumb">{t('NexAgriTech workspace')} <span>/</span> <b>{t('Overview')}</b></div><div className="top-actions"><label className="language-select"><span>◎</span><select aria-label="Change language" value={lang} onChange={e=>setLang(e.target.value)}><option value="en">English</option><option value="te">తెలుగు</option><option value="hi">हिन्दी</option></select></label><Link className="basket-link" href="/marketplace/cart">{t('Basket →')}</Link><Link className="customer-nav" href={customer?'/customer/account':'/customer/login'}>{customer?customer.name:'Customer sign in'}</Link><button className="notification" aria-label="Notifications">♧<i/></button></div></header>}
