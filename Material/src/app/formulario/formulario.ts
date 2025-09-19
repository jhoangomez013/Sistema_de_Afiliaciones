import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { materialImports } from '../shared/material/material.imports';
import { Afiliacion } from '../core/models/afiliacion';
import { AfiliacionService } from '../core/services/afiliacion.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { PermisoService } from '../core/services/permiso.service';

@Component({
  selector: 'formulario',
  standalone: true,
  imports: [...materialImports, ReactiveFormsModule],
  templateUrl: './formulario.html',
  styleUrls: ['./formulario.css']
})
export class Formulario {
  form: FormGroup;
  loading = false;
  afiliacionRegistrada: Afiliacion | null = null;
  private route = inject(ActivatedRoute);
  modoEdicion = false;
  idAfiliacion: number | null = null;


  constructor(
    private fb: FormBuilder,
    private afiliacionService: AfiliacionService,
    private snackBar: MatSnackBar,
    private permisoService: PermisoService

  ) {
    this.form = this.fb.group({
      codigo_unico: ['', Validators.required],
      nombre_comercio: ['', Validators.required],
      nit: ['', Validators.required],
      direccion: ['', Validators.required],
      ciudad: ['', Validators.required],
      red_instaladora: ['', Validators.required],
      tipo_datafono: ['', Validators.required],
      telefono: [
  '',
  [
    Validators.required,
    Validators.pattern(/^\d{7,10}$/)
  ]
],

      email: ['', [Validators.required, Validators.email]]
    });
  }
ngOnInit() {
  

  this.idAfiliacion = Number(this.route.snapshot.paramMap.get('id'));
  this.modoEdicion = !!this.idAfiliacion;

  if (this.modoEdicion) {
    
    this.afiliacionService.getAfiliacionPorId(this.idAfiliacion).subscribe({
      next: (data) => this.form.patchValue(data),
      error: (err) => console.error('Error al cargar afiliación', err),
      
    });
  }
//console.log('Permisos en Formulario:', this.permisoService.tienePermiso('editar_afiliaciones'));

}

  onSubmit() {
 if (this.form.invalid) return;

  this.loading = true;
  const datos = this.form.getRawValue();

  const request = this.modoEdicion
    ? this.afiliacionService.actualizarAfiliacion(this.idAfiliacion!, datos)
    : this.afiliacionService.crearAfiliacion(datos);

  request.subscribe({
    next: (res: Afiliacion) => {
      this.loading = false;
      this.snackBar.open(
        this.modoEdicion ? 'Afiliación actualizada con éxito' : 'Afiliación registrada con éxito',
        'Cerrar',
        { duration: 3000, panelClass: ['snackbar-success'] }
      );
      this.form.reset();
    },

      error: (err: any) => {
        console.error('Error completo:', err);
console.log(this.form.getRawValue());

  this.loading = false;

  let mensaje = 'Error inesperado';

  if (typeof err.error?.detail === 'string') {
    mensaje = err.error.detail;
  } else if (typeof err.message === 'string') {
    mensaje = err.message;
  } else if (typeof err.error === 'object') {
    mensaje = JSON.stringify(err.error); // como último recurso
  }

  this.snackBar.open(mensaje, 'Cerrar', {
    duration: 4000,
    panelClass: ['snackbar-error']
  });

  if (mensaje.includes('NIT')) {
    this.form.get('nit')?.setErrors({ backend: true });
  }
}
    });
  }

tienePermiso(nombre: string): boolean {
  return this.permisoService.tienePermiso(nombre);
}

}