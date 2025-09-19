import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://localhost:8000/usuarios'; 

  constructor(private http: HttpClient) {}

  createUser(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
}


getMisPermisos(): Observable<{ permisos: string[] }> {
  return this.http.get<{ permisos: string[] }>(`${this.apiUrl}/me/permisos`);
}

}