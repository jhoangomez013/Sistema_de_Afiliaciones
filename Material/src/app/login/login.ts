import { Component } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule, FormGroup } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';
import {App} from '../app';
import { inject } from '@angular/core';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
  private appComponent = inject(App);
  form: FormGroup;
  message = '';
  loading = false;

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onLogin() {
    if (this.form.invalid) return;
    this.loading = true;
    this.message = '';

    const body = new URLSearchParams();
    body.set('username', this.form.value.email!);
    body.set('password', this.form.value.password!);

    this.http.post<{ access_token: string }>('http://localhost:8000/login', body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).subscribe({
      next: (res) => {
        localStorage.setItem('token', res.access_token);
        this.appComponent.cargarPermisos();
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.message = err.error.message;
        this.loading = false;
      }
    });
  }
}