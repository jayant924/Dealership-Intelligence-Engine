import { Component } from '@angular/core';
import { DashboardComponent } from './dashboard/dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [DashboardComponent],
  template: `<app-dashboard></app-dashboard>`,
  styles: [`
    :host { display: block; background: transparent; min-height: 100vh; }
  `]
})
export class App {}
