import { MAT_DATE_LOCALE } from "@angular/material/core";
import { provideAnimations } from "@angular/platform-browser/animations";

export const materialProviders = [
    { provide: MAT_DATE_LOCALE, useValue: 'es-CO' },
    provideAnimations()
];