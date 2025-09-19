import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class PermisoService {
  private permisos: string[] = [];

  setPermisos(permisos: string[]) {
    this.permisos = permisos;
  }

  tienePermiso(nombre: string): boolean {
    return this.permisos.includes(nombre) || this.permisos.includes('administrador_completo');
  }
}
