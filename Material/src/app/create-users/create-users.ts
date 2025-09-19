import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { UserService } from '../core/services/user.service';
import { materialImports } from '../shared/material/material.imports';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-users',
  standalone: true,
  imports: [...materialImports, ReactiveFormsModule, CommonModule],
  templateUrl: './create-users.html',
  styleUrls: ['./create-users.css']
})
export class CreateUsers implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private usersService = inject(UserService);
  private fb = inject(FormBuilder);
  private snackBar = inject(MatSnackBar);

  form = this.fb.group({
    nombre: ['', Validators.required],
    apellido: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
    rol_id: [null, Validators.required],
    oficina: ['', Validators.required]
  });

  modoEdicion = false;
  idUsuario: number | null = null;
  creating = false;
  message = '';

  ngOnInit() {
    this.idUsuario = Number(this.route.snapshot.paramMap.get('id'));
    this.modoEdicion = !!this.idUsuario;

    if (this.modoEdicion) {
        this.form.get('password')?.clearValidators();
  this.form.get('password')?.updateValueAndValidity();

      this.usersService.getUserById(this.idUsuario).subscribe({
        next: (data) => this.form.patchValue(data),
        error: (err) => console.error('Error al cargar usuario', err)
      });
    }
  }

guardar() {
  if (this.form.invalid) return;

  const datos = this.form.getRawValue();

  // Construimos el objeto final excluyendo 'password' si está vacío en modo edición
  const datosFinal = this.modoEdicion && !datos.password
    ? {
        nombre: datos.nombre,
        apellido: datos.apellido,
        email: datos.email,
        rol_id: datos.rol_id,
        oficina: datos.oficina
      }
    : datos;

  const request = this.modoEdicion
    ? this.usersService.updateUser(this.idUsuario!, datosFinal)
    : this.usersService.createUser(datosFinal);

  request.subscribe({
    next: () => {
      this.snackBar.open(
        this.modoEdicion ? 'Usuario actualizado' : 'Usuario creado',
        'Cerrar',
        { duration: 3000 }
      );
      this.router.navigate(['/users']);
    },
    error: (err) => {
      this.snackBar.open('Error: ' + (err.message || 'No se pudo guardar'), 'Cerrar', {
        duration: 4000,
        panelClass: ['snackbar-error']
      });
    }
  });
}
}