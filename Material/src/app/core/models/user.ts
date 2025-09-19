export interface User {

       id: number;
    nombre: string;
    apellido: string;
    email: string;
    rol_id: number;
    oficina: string;
}

export interface CreateUser {

   id: number | null;
    nombre: string | null;
    apellido: string | null
    email: string | null;
    rol_id: number | null;
    oficina: string | null;
}