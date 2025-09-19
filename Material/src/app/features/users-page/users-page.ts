import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { UserService } from '../../core/services/user.service';
import { map, Observable, of, tap, catchError, startWith } from 'rxjs';
import { User } from '../../core/models/user';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar } from '@angular/material/snack-bar';
import { RouterModule } from '@angular/router';
import { materialImports } from '../../shared/material/material.imports';

export interface Vm {
  loading: boolean;
  data: User[];
  error?: string;
}

@Component({
  selector: 'app-users-page',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatListModule,
    MatIconModule,
    ...materialImports
  ],
  templateUrl: './users-page.html',
  styleUrls: ['./users-page.css']
})
export class UsersPage {
  private usersService = inject(UserService);
  private snackBar = inject(MatSnackBar);

  vm$: Observable<Vm> = this.usersService.getUsers().pipe(
    map((data) => ({ loading: false, data } as Vm)),
    startWith({ loading: true, data: [] } as Vm),
    catchError((error) =>
      of({ loading: false, data: [], error: error.message } as Vm)
    )
  );

  eliminarUsuario(id: number) {
    if (confirm('¿Estás seguro de eliminar este usuario?')) {
      this.usersService.deleteUser(id).subscribe({
        next: () => {
          this.snackBar.open('Usuario eliminado', 'Cerrar', { duration: 3000 });
          // Recargar la lista después de eliminar
          this.vm$ = this.usersService.getUsers().pipe(
            map((data) => ({ loading: false, data } as Vm)),
            startWith({ loading: true, data: [] } as Vm),
            catchError((error) =>
              of({ loading: false, data: [], error: error.message } as Vm)
            )
          );
        },
        error: (err) => {
          this.snackBar.open('Error al eliminar usuario', 'Cerrar', {
            duration: 4000,
            panelClass: ['snackbar-error']
          });
          console.error('Error al eliminar:', err);
        }
      });
    }
  }
}