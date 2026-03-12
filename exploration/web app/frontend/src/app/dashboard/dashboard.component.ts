import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  IntelligenceService,
  DealershipTrend,
  DealershipSeasonality,
} from '../services/intelligence.service';
import { TrendChartComponent } from '../charts/trend-chart.component';
import { SeasonalityChartComponent } from '../charts/seasonality-chart.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, TrendChartComponent, SeasonalityChartComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
  trends: DealershipTrend[] = [];
  seasonalities: DealershipSeasonality[] = [];
  selectedSeasonality!: DealershipSeasonality;
  loading = true;
  error = '';

  readonly classColors: Record<string, string> = {
    CHAMPION: '#27ae60',
    STRAGGLER: '#e74c3c',
    'AT RISK': '#f39c12',
    RECOVERING: '#2980b9',
  };

  constructor(private svc: IntelligenceService) {}

  ngOnInit() {
    this.svc.getTrends().subscribe({
      next: res => {
        this.trends = res.dealerships;
        this.checkLoaded();
      },
      error: () => (this.error = 'Failed to load trends. Is the backend running?'),
    });

    this.svc.getAllSeasonality().subscribe({
      next: res => {
        this.seasonalities = res.dealerships;
        this.selectedSeasonality = res.dealerships[0];
        this.checkLoaded();
      },
      error: () => (this.error = 'Failed to load seasonality. Is the backend running?'),
    });
  }

  private checkLoaded() {
    if (this.trends.length && this.seasonalities.length) {
      this.loading = false;
    }
  }

  selectSeasonality(name: string) {
    const found = this.seasonalities.find(s => s.dealership === name);
    if (found) this.selectedSeasonality = found;
  }

  classColor(label: string): string {
    return this.classColors[label] ?? '#555';
  }
}
