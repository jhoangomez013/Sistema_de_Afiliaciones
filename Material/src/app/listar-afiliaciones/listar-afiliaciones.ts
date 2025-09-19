import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AfiliacionService } from '../core/services/afiliacion.service';
import { MatTableModule } from '@angular/material/table';
import { MatTableDataSource } from '@angular/material/table';
import { materialImports } from '../shared/material/material.imports';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { PermisoService } from '../core/services/permiso.service';

@Component({
  selector: 'app-listar-afiliaciones',
  standalone: true,
  imports: [...materialImports, CommonModule, MatTableModule],
  templateUrl: './listar-afiliaciones.html',
  styleUrls: ['./listar-afiliaciones.css']
})
export class ListarAfiliaciones implements OnInit {
    permisos: string[] = [];
  private afiliacionService = inject(AfiliacionService);
  private http = inject(HttpClient);
  afiliaciones = new MatTableDataSource<any>();

  displayedColumns = [
    'codigo',
    'comercio',
    'nit',
    'direccion',
    'ciudad',
    'red_instaladora',
    'tipo_datafono',
    'telefono',
    'email',
    'registrado_por',
    ...(this.tienePermiso('editar_afiliaciones') ? ['acciones'] : [])
  ];

  ngOnInit() {
    this.afiliacionService.getAfiliaciones().subscribe({
      next: (data) => {
        this.afiliaciones.data = data;
      },
      error: (err) => console.error('Error al cargar afiliaciones', err)
    });
  }

  filtrarPorUsuario(event: Event) {
    const valor = (event.target as HTMLInputElement).value.trim().toLowerCase();
    this.afiliaciones.filterPredicate = (afiliacion, filtro) => {
      const nombre = afiliacion.usuario?.nombre?.toLowerCase() || '';
      const apellido = afiliacion.usuario?.apellido?.toLowerCase() || '';
      return nombre.includes(filtro) || apellido.includes(filtro);
    };
    this.afiliaciones.filter = valor;
  }

eliminarAfiliacion(id: number) {

  if (confirm('¿Estás seguro de eliminar esta afiliación?')) {

  this.afiliacionService.eliminarAfiliacion(id).subscribe({
    next: () => {
      this.afiliaciones.data = this.afiliaciones.data.filter((a: any) => a.id !== id);
      console.log(`Afiliación ${id} eliminada`);
    },
    error: (err) => console.error('Error al eliminar afiliación', err)
  });
}
}
tienePermiso(nombre: string): boolean {

  return this.permisos.includes(nombre) || this.permisos.includes('administrador_completo');
}
  descargarCSV() {
    this.afiliacionService.descargarCSV().subscribe(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'afiliaciones.csv';
      a.click();
      window.URL.revokeObjectURL(url);
    });
  }
}