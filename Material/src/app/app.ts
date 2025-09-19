import { Component, OnInit } from '@angular/core';
import { materialImports } from './shared/material/material.imports';
import { RouterModule, Router } from '@angular/router';
import { RouterOutlet } from '@angular/router';
import { AuthService } from './core/services/auth.service'; 
import { ChangeDetectorRef } from '@angular/core';
import { PermisoService } from './core/services/permiso.service';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [...materialImports, RouterOutlet, RouterModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  title = 'Sistema de Afiliaciones';
  permisos: string[] = [];

  constructor(public router: Router, private authService: AuthService, private cd: ChangeDetectorRef,private permisoService: PermisoService
) {}

ngOnInit(): void {
  this.cargarPermisos();
  if (this.usuarioAutenticado()) {
    this.authService.getMisPermisos().subscribe(res => {
      this.permisos = res.permisos;
      this.permisoService.setPermisos(res.permisos);
      //console.log('Permisos cargados:', this.permisos);
      this.cd.detectChanges();
    });
  }
}




  mostrarLayoutCompleto(): boolean {
    return this.router.url !== '/login';
  }

  mostrarSoloBarraYFooter(): boolean {
    return true;
  }

  usuarioAutenticado(): boolean {
    return !!localStorage.getItem('token');
  }

  cerrarSesion(): void {
    localStorage.removeItem('token');
    this.permisoService.setPermisos([]);
    this.router.navigate(['/login']);
  }

tienePermiso(nombre: string): boolean {

  return this.permisos.includes(nombre) || this.permisos.includes('administrador_completo');
}

cargarPermisos(): void {
  if (this.usuarioAutenticado()) {
    this.authService.getMisPermisos().subscribe(res => {
      this.permisos = res.permisos;
      this.permisoService.setPermisos(res.permisos);
      //console.log('Permisos cargados:', this.permisos);
      this.cd.detectChanges();
    });
  }
}

}
