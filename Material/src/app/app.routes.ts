import { Routes } from '@angular/router';
import { UsersPage } from './features/users-page/users-page';
import { Formulario } from './formulario/formulario';
import { CreateUsers } from './create-users/create-users';
import { Login } from './login/login';
import { ListarAfiliaciones } from './listar-afiliaciones/listar-afiliaciones';
import { Inicio } from './inicio/inicio';
import { AuthGuard } from './auth-guard'; 
import { App } from './app';

export const routes: Routes = [
  {
    path: '',
    children: [
      { path: '', component: Inicio, canActivate: [AuthGuard] },
      { path: 'users', component: UsersPage, canActivate: [AuthGuard] },
      { path: 'users/create', component: CreateUsers, canActivate: [AuthGuard] },
      { path: 'afiliaciones/create', component: Formulario, canActivate: [AuthGuard] },
      { path: 'afiliaciones/list', component: ListarAfiliaciones, canActivate: [AuthGuard] },
      { path: 'login', component: Login } ,
      { path: 'afiliaciones/create/:id', component: Formulario, canActivate: [AuthGuard] },
      { path: 'users/edit/:id', component: CreateUsers, canActivate: [AuthGuard] }

    ]
  }
];


