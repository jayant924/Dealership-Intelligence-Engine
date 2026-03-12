import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PeriodComparison {
  prev_avg: number;
  recent_avg: number;
  change: number;
  change_pct: number;
}

export interface Classification {
  label: string;
  reason: string;
}

export interface DealershipTrend {
  name: string;
  months: number[];
  revenue: number[];
  trend_line: number[];
  moving_average: (number | null)[];
  slope: number;
  period_comparison: PeriodComparison;
  classification: Classification;
}

export interface TrendsResponse {
  dealerships: DealershipTrend[];
}

export interface SeasonalitySummary {
  model: string;
  period: number;
  seasonal_strength_pct: number;
  peak_month: number;
  trough_month: number;
}

export interface DealershipSeasonality {
  dealership: string;
  months: number[];
  observed: number[];
  trend: (number | null)[];
  seasonal: (number | null)[];
  residual: (number | null)[];
  summary: SeasonalitySummary;
}

export interface SeasonalityResponse {
  dealerships: DealershipSeasonality[];
}

@Injectable({ providedIn: 'root' })
export class IntelligenceService {
  private base = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getTrends(): Observable<TrendsResponse> {
    return this.http.get<TrendsResponse>(`${this.base}/api/trends/`);
  }

  getTrend(dealership: string): Observable<DealershipTrend> {
    return this.http.get<DealershipTrend>(`${this.base}/api/trends/${dealership}`);
  }

  getAllSeasonality(): Observable<SeasonalityResponse> {
    return this.http.get<SeasonalityResponse>(`${this.base}/api/seasonality/`);
  }

  getSeasonality(dealership: string): Observable<DealershipSeasonality> {
    return this.http.get<DealershipSeasonality>(`${this.base}/api/seasonality/${dealership}`);
  }
}
