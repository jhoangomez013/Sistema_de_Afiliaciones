import { NgModule } from "@angular/core";
import {MAT_DATE_LOCALE} from "@angular/material/core";

export const MY_DATE_FORMATS = {
    parse: {datteInput: 'DD/MM/YYYY'},
    display: {
    monthYearLabel: 'MMM YYYY',
   dateA11yLabel: 'LL',
}};

@NgModule({
    providers: [
        {provide: MAT_DATE_LOCALE, useValue: 'es-CO'},
     //   {provide: MAT_DATE_FORMATS, useValue: MY_DATE_FORMATS}
    ]

})
export class CoreModule { }