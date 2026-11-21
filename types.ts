export type Farmer={id:number;name:string;farm_name:string;location:string;acres:number;language:string};
export type Crop={id:number;name:string;variety:string;acres:number;stage:string;planted_on:string};
export type Product={id:number;name:string;category:string;price:number;quantity:number;unit:string;description:string;harvest_date:string;practices:string;certification:string;nutrition:string;emoji:string;farmer:string;location:string};
export type State={farmer:Farmer|null;crops:Crop[];products:Product[];tasks:any[];orders:any[];prices:any[];advice:any[];lessons:any[]};
