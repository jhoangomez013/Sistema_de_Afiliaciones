import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Afiliacion } from '../models/afiliacion';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AfiliacionService {
  private apiUrl = 'http://localhost:8000/afiliaciones';
  private reportesUrl = 'http://localhost:8000/reportes';

  constructor(private http: HttpClient) {}

  crearAfiliacion(data: Afiliacion): Observable<Afiliacion> {
    return this.http.post<Afiliacion>(this.apiUrl, data);
  }

  getAfiliaciones(): Observable<Afiliacion[]> {
    return this.http.get<Afiliacion[]>(this.apiUrl);
  }

  eliminarAfiliacion(id: number) : Observable<any> {
  return this.http.delete(`${this.apiUrl}/${id}`);

}

  getAfiliacionPorId(id: number): Observable<Afiliacion> {
  return this.http.get<Afiliacion>(`${this.apiUrl}/${id}`);
}

actualizarAfiliacion(id: number, data: Afiliacion): Observable<Afiliacion> {
  return this.http.put<Afiliacion>(`${this.apiUrl}/${id}`, data);
}

  descargarCSV(): Observable<Blob> {
    return this.http.get(`${this.reportesUrl}/afiliaciones/csv`, {
      responseType: 'blob'
    });
  }




}



